import io
import pickle
from datetime import datetime
from pdf2image import convert_from_bytes
import boto3
import os
from .models import conectar_db

conexao = conectar_db()

def obter_valores_atuais(id_pdf):
    try:
        with conexao.cursor() as cursor:
            sql = "SELECT name, location, page_images FROM pdf WHERE id_pdf = %s"
            cursor.execute(sql, (id_pdf,))
            resultado = cursor.fetchone()
            if resultado:
                return resultado
            else:
                return None, None, None
    except Exception as e:
        print(f"Erro ao obter valores atuais: {e}")
        return None, None, None

def renomear_pasta_s3(nome_antigo, nome_novo):
    # Recuperar o nome do bucket das variáveis de ambiente
    bucket_name = os.getenv("BUCKET_NAME")

    s3_client = boto3.client('s3',
                             aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                             aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))

    # Verifica se a pasta com o nome antigo existe
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=f'Documents/{nome_antigo}/')

    if 'Contents' in response:
        # Renomeia a pasta para o novo nome
        for obj in response['Contents']:
            novo_key = obj['Key'].replace(nome_antigo, nome_novo, 1)
            s3_client.copy_object(Bucket=bucket_name, CopySource=f"{bucket_name}/{obj['Key']}", Key=novo_key)
            s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])

def fazer_upload_para_s3(nome, versao, conteudo_arquivo):
    if conteudo_arquivo:
        # Recuperar o nome do bucket das variáveis de ambiente
        bucket_name = os.getenv("BUCKET_NAME")
        
        s3_client = boto3.client('s3',
                                 aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                                 aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))
        key = f'Documents/{nome}/{nome}_{versao}.pdf'
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=conteudo_arquivo)

def converter_pdf_para_imagens(conteudo_arquivo):
    imagens = convert_from_bytes(conteudo_arquivo)
    return imagens

def converter_imagem_para_binario(imagem):
    buf = io.BytesIO()
    imagem.save(buf, format='PNG')
    conteudo_binario = buf.getvalue()
    buf.close()
    return conteudo_binario

def pdf_edit(id_pdf, nome, categoria, data, arquivo):
    try:
        valor_atual_nome, valor_atual_location, valor_atual_page_images = obter_valores_atuais(id_pdf)

        if nome != valor_atual_nome:
            # Se o nome do documento foi alterado, renomeia a pasta no S3
            renomear_pasta_s3(valor_atual_nome, nome)

        if arquivo:
            conteudo_arquivo = arquivo.read()  # Lê o conteúdo do arquivo como binário
            imagens = converter_pdf_para_imagens(conteudo_arquivo)
            imagens_binarias = [converter_imagem_para_binario(imagem) for imagem in imagens]
            imagens_agrupadas = pickle.dumps(imagens_binarias)
            
            # Faz o upload do novo arquivo para o S3
            fazer_upload_para_s3(nome, valor_atual_nome, conteudo_arquivo)
        else:
            # Mantém os valores atuais se um novo arquivo não for enviado
            conteudo_arquivo = valor_atual_location
            imagens_agrupadas = valor_atual_page_images

        if data:
            data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        else:
            data_formatada = None

        # Atualiza o registro no banco de dados
        salvar_no_banco_de_dados(id_pdf, nome, categoria, data_formatada, conteudo_arquivo, imagens_agrupadas)

    except Exception as e:
        print(f"Erro ao processar o formulário: {e}")

def salvar_no_banco_de_dados(id_pdf, nome, categoria, data, conteudo_arquivo, imagens_agrupadas):
    try:
        with conexao.cursor() as cursor:
            sql = "UPDATE pdf SET name = %s, category = %s, location = %s, date = %s, page_images = %s WHERE id_pdf = %s"
            cursor.execute(sql, (nome, categoria, conteudo_arquivo, data, imagens_agrupadas, id_pdf))

        conexao.commit()
        print("Atualização no banco de dados bem-sucedida!")
    except Exception as e:
        print(f"Erro ao atualizar no banco de dados: {e}")
