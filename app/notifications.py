from flask import Flask, session
from .models import conectar_db
import pymysql.cursors  # define o retorno como uma lista

app = Flask(__name__)

def get_notifications():
    # Obtém a conexão com o banco de dados
    conexao = conectar_db()

    with conexao.cursor(pymysql.cursors.DictCursor) as cursor:  # Usa DictCursor
        sql = """
                SELECT n.*, p.name AS pdf_name, p.version AS pdf_version
                FROM notifications n
                INNER JOIN pdf p ON n.id_pdf = p.id_pdf
                INNER JOIN user_notifications un ON n.id_notifications = un.id_notifications
                WHERE un.id_user = %s
                AND un.read = FALSE
                ORDER BY n.time DESC;
            """
        cursor.execute(sql, (session['id_user'],))
        notifications = cursor.fetchall()
    return notifications
