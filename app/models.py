import os
import pymysql
import logging

# Configurações de conexão
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def conectar_db():
    try:
        # Configurações de conexão
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5,
            read_timeout=30,
            write_timeout=30,
            charset='utf8mb4',
            use_unicode=True
        )
        connection.ping(reconnect=True)  # Checa a conexão e tenta reconectar se necessário
        logging.info("Conexão com o banco de dados estabelecida com sucesso.")
        return connection
    except pymysql.Error as err:
        logging.error(f"Erro ao conectar ao banco de dados: {err}")
        return None