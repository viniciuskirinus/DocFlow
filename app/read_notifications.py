from flask import session
from .models import conectar_db
import pymysql.cursors

def marcar_todas_como_lidas():
    # Obtém a conexão com o banco de dados
    conexao = conectar_db()

    with conexao.cursor() as cursor:
        sql = """
                UPDATE user_notifications
                SET `read` = TRUE
                WHERE id_user = %s
            """
        cursor.execute(sql, (session['id_user'],))
        conexao.commit()

    # Retornando uma string vazia, pois não queremos redirecionar
    return ''