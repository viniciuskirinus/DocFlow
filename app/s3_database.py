import boto3
import os

def list_folders_and_files(bucket_name, folder_name=''):
    access_key_id = os.getenv("ACCESS_KEY_ID")
    secret_access_key = os.getenv("SECRET_ACCESS_KEY")

    s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    response = s3.list_objects_v2(Bucket=bucket_name, Delimiter='/', Prefix=folder_name)

    folders = []
    files = []

    # Listar pastas e arquivos
    for obj in response.get('CommonPrefixes', []):
        folders.append(obj.get('Prefix'))

    for obj in response.get('Contents', []):
        files.append(obj.get('Key'))

    # Percorrer subpastas recursivamente
    for folder in folders:
        subfolders, subfiles = list_folders_and_files(bucket_name, folder)
        folders.extend(subfolders)
        files.extend(subfiles)

    return folders, files