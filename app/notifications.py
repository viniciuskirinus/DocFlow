from flask import Flask
from .models import conectar_db

app = Flask(__name__)

def get_notifications():

    # Obtém a conexão com o banco de dados
    conexao = conectar_db()
    cursor = conexao.cursor()
    
    with conexao.cursor() as cursor:
        sql = """
        SELECT n.*, p.name AS pdf_name, p.version AS pdf_version
        FROM notifications n
        INNER JOIN pdf p ON n.id_pdf = p.id
        ORDER BY n.time DESC
        """
        cursor.execute(sql)
        notifications = cursor.fetchall()
    return notifications