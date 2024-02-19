import os
from datetime import datetime
import hashlib
from .models import conectar_db

conexao = conectar_db()

def processar_formulario_user(nome, cargo, role, senha):
    try:
        senha_md5 = hashlib.md5(senha.encode()).hexdigest() 
        salvar_no_banco_de_dados(nome, cargo, role, senha_md5)

    except Exception as e:
        print(f"Erro ao processar o formulário: {e}")

def salvar_no_banco_de_dados(nome, cargo, role, senha):
    try:
        # Insere no banco de dados
        with conexao.cursor() as cursor:
            sql = "INSERT INTO user (account, office, password, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nome, cargo, senha, role))

        # Commit para efetivar a operação no banco de dados
        conexao.commit()
        print("Inserção no banco de dados bem-sucedida!")
    except Exception as e:
        print(f"Erro ao inserir no banco de dados: {e}")
