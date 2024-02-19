import pymysql
import hashlib
from .models import conectar_db
from datetime import datetime, timedelta
from flask import session


def processar_login(username, password):

    conexao = conectar_db()

    if conexao:
        try:
            with conexao.cursor() as cursor:
                # Consulta parametrizada para obter o hash MD5 da senha associada ao username
                sql = "SELECT password, role, office FROM user WHERE account = %s;"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()

                if result:
                    # Verifica se a senha fornecida corresponde ao hash armazenado no banco de dados
                    senha_hash_db, user_role, user_office = result
                    senha_hash_fornecida = hashlib.md5(password.encode()).hexdigest()

                    if senha_hash_db == senha_hash_fornecida:
                        # Adicione o username, a função e o office à sessão para serem acessíveis nas rotas
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
