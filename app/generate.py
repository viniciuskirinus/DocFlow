import io
import pickle
import boto3
from datetime import datetime
from pdf2image import convert_from_bytes
from .models import conectar_db
import os

conexao = conectar_db()

def verificar_documento_existente(nome):
    try:
        with conexao.cursor() as cursor:
            sql_verificar = "SELECT name FROM pdf WHERE name = %s"
            cursor.execute(sql_verificar, (nome,))
            resultado = cursor.fetchone()
            return bool(resultado)  # Retorna True se documento existir, False caso contrário
    except Exception as e:
        raise RuntimeError("Erro ao verificar a existência do documento")

def processar_formulario(nome, categoria, versao, data, setor, arquivo):
    try:
        if verificar_documento_existente(nome):
            return False  # Documento já existe, portanto, retorno False
        
        conteudo_arquivo = arquivo.read()
        imagens = convert_from_bytes(conteudo_arquivo)
        imagens_binarias = [converter_imagem_para_binario(imagem) for imagem in imagens]
        imagens_agrupadas = pickle.dumps(imagens_binarias)

        # Salva no banco de dados
        if not salvar_no_banco_de_dados(nome, categoria, setor, data, versao, conteudo_arquivo, imagens_agrupadas):
            raise RuntimeError("Falha ao salvar no banco de dados")

        criar_pasta_s3(nome)
        fazer_upload_para_s3(nome, versao, conteudo_arquivo)
        
        return True
    except Exception as e:
        raise RuntimeError("Erro ao processar o formulário: " + str(e))
    

def converter_imagem_para_binario(imagem):
    buf = io.BytesIO()
    imagem.save(buf, format='PNG')
    conteudo_binario = buf.getvalue()
    buf.close()
    return conteudo_binario

def salvar_no_banco_de_dados(nome, categoria, setor, data, versao, conteudo_arquivo, imagens_agrupadas):
    try:
        data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        with conexao.cursor() as cursor:
            sql_inserir = "INSERT INTO pdf (name, category, sector, version, location, date, page_images) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_inserir, (nome, categoria, setor, versao, conteudo_arquivo, data_formatada, imagens_agrupadas))
            
            # Recuperando o ID do PDF recém-inserido
            ultimo_id_inserido = cursor.lastrowid
            
            # Inserindo dados na tabela de notificações
            sql_inserir_notificacao = "INSERT INTO notifications (description, time, read, id_pdf) VALUES (%s, %s, %s, %s)"
            descricao = "Novo documento lançado no portal"
            cursor.execute(sql_inserir_notificacao, (descricao, data_formatada, False, ultimo_id_inserido))

        conexao.commit()
        return True
    except Exception as e:
        return False

def criar_pasta_s3(nome):
    bucket_name = os.getenv("BUCKET_NAME")
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                             aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))
    s3_client.put_object(Bucket=bucket_name, Key=f'Documents/{nome}/')

def fazer_upload_para_s3(nome, versao, conteudo_arquivo):
    bucket_name = os.getenv("BUCKET_NAME")
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                             aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))
    key = f'Documents/{nome}/{nome}_{versao}.pdf'
    s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=conteudo_arquivo,
        ContentType='application/pdf'  
    )
