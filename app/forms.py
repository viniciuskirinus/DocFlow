import hashlib
from .models import conectar_db
from flask import session
import pymysql
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

def processar_login(username, password):
    conexao = conectar_db()

    if conexao:
        try:
            with conexao.cursor() as cursor:
                sql = "SELECT id_user, password, role, office FROM user WHERE account = %s;"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()

                if result:
                    id_user, senha_hash_db, user_role, user_office = result
                    senha_hash_fornecida = hashlib.sha256(password.encode()).hexdigest()

                    if senha_hash_db == senha_hash_fornecida:
                        sql_update_access = "UPDATE user SET access = %s WHERE account = %s;"
                        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        cursor.execute(sql_update_access, (current_datetime, username))

                        session['id_user'] = id_user
                        session['role'] = user_role
                        session['username'] = username
                        session['office'] = user_office
                        logging.info("Login bem-sucedido!")
                        return "Login bem-sucedido!"
                    else:
                        logging.warning("Falha no login: senha incorreta.")
                        return "Falha no login: Verifique as informações."
                else:
                    logging.warning("Falha no login: usuário não encontrado.")
                    return "Falha no login: Verifique as informações."

        except pymysql.Error as err:
            logging.error(f"Falha no login: Erro durante a execução da consulta: {err}")
            return f"Falha no login: Erro durante a execução da consulta: {err}"

        finally:
            conexao.close()

    logging.error("Falha no login: Erro na conexão com o banco de dados.")
    return "Falha no login: Erro na conexão com o banco de dados."