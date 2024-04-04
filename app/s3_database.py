import boto3
import os

def list_folders_and_files(bucket_name, folder_name=''):
    access_key_id = os.getenv("ACCESS_KEY_ID")
    secret_access_key = os.getenv("SECRET_ACCESS_KEY")

    s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    
    # Primeiro, listar todas as subpastas dentro de 'Documents/'
    response = s3.list_objects_v2(Bucket=bucket_name, Delimiter='/', Prefix=folder_name)
    folders = [obj.get('Prefix') for obj in response.get('CommonPrefixes', [])]
    
    files_dict = {}
    
    # Para cada subpasta encontrada, listar todos os arquivos
    for folder in folders:
        subresponse = s3.list_objects_v2(Bucket=bucket_name, Delimiter='/', Prefix=folder)
        files = []
        for obj in subresponse.get('Contents', []):
            file_key = obj['Key']
            # Garantir que estamos adicionando apenas arquivos, não subpastas
            if not file_key.endswith('/'):
                file_url = f"https://{bucket_name}.s3.amazonaws.com/{file_key}"
                files.append({'name': file_key.split('/')[-1], 'url': file_url})
                
        # Associar os arquivos encontrados com a subpasta correspondente
        files_dict[folder] = files

    return folders, files_dict
