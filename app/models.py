import os
import pymysql

# Configurações de conexão
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

# Criar uma conexão
def conectar_db():
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            autocommit=True
        )
        return connection

    except pymysql.Error as err:
        print(f"Erro de conexão: {err}")
        return None