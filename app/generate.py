import io
import pickle
import boto3
from datetime import datetime
from pdf2image import convert_from_bytes
from .models import conectar_db
import os

conexao = conectar_db()

class ProcessamentoErro(Exception):
    def __init__(self, message):
        self.message = message

def verificar_documento_existente(nome):
    try:
        with conexao.cursor() as cursor:
            sql_verificar = "SELECT name FROM pdf WHERE name = %s"
            cursor.execute(sql_verificar, (nome,))
            resultado = cursor.fetchone()
            if resultado:
                return True  # Documento com o mesmo nome encontrado
            else:
                return False  # Documento não encontrado
    except Exception as e:
        raise ProcessamentoErro("Erro ao verificar a existência do documento")

def processar_formulario(nome, categoria, versao, data, setor, arquivo):
    try:
        if verificar_documento_existente(nome):
            raise ProcessamentoErro("Já existe um documento cadastrado com este nome.")
        
        conteudo_arquivo = arquivo.read()
        imagens = converter_pdf_para_imagens(conteudo_arquivo)
        imagens_binarias = [converter_imagem_para_binario(imagem) for imagem in imagens]
        imagens_agrupadas = pickle.dumps(imagens_binarias)

        # Salva no banco de dados
        if not salvar_no_banco_de_dados(nome, categoria, setor, data, versao, conteudo_arquivo, imagens_agrupadas):
            raise ProcessamentoErro("Falha ao salvar no banco de dados")

        criar_pasta_s3(nome)
        fazer_upload_para_s3(nome, versao, conteudo_arquivo)
        
        return True
    except ProcessamentoErro as e:
        raise e
    except Exception as e:
        raise ProcessamentoErro("Erro desconhecido ao processar o formulário")

def converter_pdf_para_imagens(conteudo_arquivo):
    # Converte o conteúdo do PDF (em bytes) para uma lista de imagens
    imagens = convert_from_bytes(conteudo_arquivo)
    return imagens

def converter_imagem_para_binario(imagem):
    # Converte a imagem para um formato binário
    buf = io.BytesIO()
    imagem.save(buf, format='PNG')
    conteudo_binario = buf.getvalue()
    buf.close()
    return conteudo_binario

def salvar_no_banco_de_dados(nome, categoria, setor, data, versao, conteudo_arquivo, imagens_agrupadas):
    try:
        # Converte a data para o formato do banco de dados
        data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')

        with conexao.cursor() as cursor:
            # Insere os dados no banco de dados
            sql_inserir = "INSERT INTO pdf (name, category, sector, version, location, date, page_images) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_inserir, (nome, categoria, setor, versao, conteudo_arquivo, data_formatada, imagens_agrupadas))

        conexao.commit()
        return True
    except Exception as e:
        return False

def criar_pasta_s3(nome):
    # Recuperar o nome do bucket das variáveis de ambiente
    bucket_name = os.getenv("BUCKET_NAME")
    
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                             aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))
    s3_client.put_object(Bucket=bucket_name, Key=f'Documents/{nome}/')

def fazer_upload_para_s3(nome, versao, conteudo_arquivo):
    # Recuperar o nome do bucket das variáveis de ambiente
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
