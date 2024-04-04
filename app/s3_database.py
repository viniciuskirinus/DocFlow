import boto3
import os

def list_folders_and_files(bucket_name, folder_name=''):
    access_key_id = os.getenv("ACCESS_KEY_ID")
    secret_access_key = os.getenv("SECRET_ACCESS_KEY")

    s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    response = s3.list_objects_v2(Bucket=bucket_name, Delimiter='/', Prefix=folder_name)

    folders = []
    files_dict = {}

    # Listar pastas
    for obj in response.get('CommonPrefixes', []):
        folders.append(obj.get('Prefix'))
        # Inicializar cada pasta no dicionário de arquivos
        files_dict[obj.get('Prefix')] = []

    # Listar arquivos
    for obj in response.get('Contents', []):
        key = obj.get('Key')
        folder_key = '/'.join(key.split('/')[:-1]) + '/'
        if folder_key in files_dict:
            # Se a pasta já existe no dicionário, adicione o arquivo
            files_dict[folder_key].append({
                'name': key.split('/')[-1],
                'url': f"https://{bucket_name}.s3.amazonaws.com/{key}"  #
            })
        else:
            # Caso contrário, crie uma nova entrada para arquivos soltos na raiz (se necessário)
            if folder_key == folder_name:
                if folder_name not in files_dict:
                    files_dict[folder_name] = []
                files_dict[folder_name].append({
                    'name': key.split('/')[-1],
                    'url': f"https://{bucket_name}.s3.amazonaws.com/{key}"  
                })


    return folders, files_dict
