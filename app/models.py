import pymysql

# Configurações de conexão
host = "localhost"
user = "root"
password = ""
database = "doc_flow_db"

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