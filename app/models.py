import pymysql

# Configurações de conexão
host = "localhost"
user = "u369946143_sirtec_docflow"
password = "af!Inf30"
database = "u369946143_doc_flow"

# Criar uma conexão
def conectar_db():
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection

    except pymysql.Error as err:
        print(f"Erro de conexão: {err}")
        return None