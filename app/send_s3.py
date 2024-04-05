import os
import boto3

def send_s3(folder, file):
    # Configuração do cliente S3
    s3 = boto3.client('s3', aws_access_key_id=os.getenv("ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))

    # Nome do bucket
    bucket_name = os.getenv("BUCKET_NAME")

    # Nome do arquivo no S3 (pode ser o mesmo nome do arquivo enviado)
    file_name = file.filename

    # Definindo o Content-Type do arquivo
    content_type = 'application/pdf'

    # Upload do arquivo para o S3
    try:
        s3.upload_fileobj(file, bucket_name, f'{folder}/{file_name}', ExtraArgs={'ContentType': content_type})
        print(f'Arquivo {file_name} enviado para o bucket {bucket_name} na pasta {folder} com sucesso.')
    except Exception as e:
        print(f'Erro ao enviar arquivo para o S3: {e}')
