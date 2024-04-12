import os
import boto3

def send_s3(folder, files, file_names):
    # Configuração do cliente S3
    
    # Nome do bucket
    bucket_name = os.getenv("BUCKET_NAME")

    # Definindo o Content-Type dos arquivos
    content_type = 'application/pdf'  # Defina o tipo de conteúdo apropriado aqui

    # Configuração do cliente S3
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                             aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))

    # Iterar sobre os arquivos e enviá-los para o S3
    for file, file_name in zip(files, file_names):
        try:
            key = f'{folder}{file_name}'
            # Obtenha os dados do arquivo
            s3_client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=file,
                ContentType=content_type
            )
            print(f'Arquivo {file_name} enviado para o bucket {bucket_name} na pasta {folder} com sucesso.')
        except Exception as e:
            print(f'Erro ao enviar arquivo {file_name} para o S3: {e}')
