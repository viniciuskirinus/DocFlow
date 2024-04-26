import hashlib
from .models import conectar_db
from flask import session
import pymysql
from datetime import datetime

def processar_login(username, password):
    conexao = conectar_db()

    if conexao:
        try:
            with conexao.cursor() as cursor:
                # Consulta parametrizada para obter o hash SHA-256 da senha associada ao username
                sql = "SELECT id_user, password, role, office FROM user WHERE account = %s;"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()

                if result:
                    # Verifica se a senha fornecida corresponde ao hash armazenado no banco de dados
                    id_user, senha_hash_db, user_role, user_office = result
                    senha_hash_fornecida = hashlib.sha256(password.encode()).hexdigest()

                    if senha_hash_db == senha_hash_fornecida:
                        # Atualiza a coluna de acesso com a data e hora atuais
                        sql_update_access = "UPDATE user SET access = %s WHERE account = %s;"
                        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        cursor.execute(sql_update_access, (current_datetime, username))

                        # Adicione o id_user, username, a função e o office à sessão para serem acessíveis nas rotas
                        session['id_user'] = id_user
                        session['role'] = user_role
                        session['username'] = username
                        session['office'] = user_office
                        return "Login bem-sucedido!"
                    else:
                        return "Falha no login: Verifique as informações."
                else:
                    return "Falha no login: Verifique as informações."

        except pymysql.Error as err:
            return f"Falha no login: Erro durante a execução da consulta: {err}"

        finally:
            # Fecha a conexão após o uso
            conexao.close()

    return "Falha no login: Erro na conexão com o banco de dados."
