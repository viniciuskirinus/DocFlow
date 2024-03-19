import pymysql

# Configurações de conexão
host = "srv539.hstgr.io"
user = "u369946143_sirflow"
password = "Sirtec#411"
database = "u369946143_doc_flow_db"

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