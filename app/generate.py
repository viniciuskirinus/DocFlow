import io
import pickle
import boto3
from datetime import datetime
from pdf2image import convert_from_bytes
from .models import conectar_db
import os

conexao = conectar_db()

def processar_formulario(nome, categoria, versao, data, setor, arquivo):
    try:
        # Gera um nome para o arquivo baseado na categoria e na data/hora atual
        conteudo_arquivo = arquivo.read()  # Lê o conteúdo do arquivo como binário
        imagens = converter_pdf_para_imagens(conteudo_arquivo)

        # Converte todas as imagens para binário e as agrupa
        imagens_binarias = [converter_imagem_para_binario(imagem) for imagem in imagens]
        imagens_agrupadas = pickle.dumps(imagens_binarias)

        # Salva no banco de dados
        salvar_no_banco_de_dados(nome, categoria, setor, data, versao, conteudo_arquivo, imagens_agrupadas)

        # Cria a pasta no S3
        criar_pasta_s3(nome)

        # Faz o upload do arquivo para o S3
        fazer_upload_para_s3(nome, versao, conteudo_arquivo)
        return True
    except Exception as e:
        print(f"Erro ao processar o formulário: {e}")
        return False

def converter_pdf_para_imagens(conteudo_arquivo):
    # Converte o conteúdo do PDF (em bytes) para uma lista de imagens
    imagens = convert_from_bytes(conteudo_arquivo)
    return imagens

def converter_imagem_para_binario(imagem):
    # Converte a imagem para um formato binário (por exemplo, PNG)
    buf = io.BytesIO()
    imagem.save(buf, format='PNG')
    conteudo_binario = buf.getvalue()
    buf.close()
    return conteudo_binario

def salvar_no_banco_de_dados(nome, categoria, setor, data, versao, conteudo_arquivo, imagens_agrupadas):
    try:
        # Converte a data para o formato do banco de dados
        data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')

        # Ajuste conforme sua estrutura de banco de dados
        with conexao.cursor() as cursor:
            sql = "INSERT INTO pdf (name, category, sector, version, location, date, page_images) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (nome, categoria, setor, versao, conteudo_arquivo, data_formatada, imagens_agrupadas))

        conexao.commit()
        print("Inserção no banco de dados bem-sucedida!")
        return True
    except Exception as e:
        print(f"Erro ao inserir no banco de dados: {e}")
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
        ContentType='application/pdf'  # Adicionando o ContentType
    )
