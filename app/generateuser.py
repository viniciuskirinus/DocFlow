from datetime import datetime
import hashlib
from .models import conectar_db

conexao = conectar_db()

def verificar_usuario_existente(nome):
    try:
        with conexao.cursor() as cursor:
            sql_verificar = "SELECT account FROM user WHERE account = %s"
            cursor.execute(sql_verificar, (nome,))
            resultado = cursor.fetchone()
            return bool(resultado)  # Retorna True se documento existir, False caso contrário
    except Exception as e:
        raise RuntimeError("Erro ao verificar a existência do usuário")


def processar_formulario_user(nome, cargo, role, senha):
    try:
        if verificar_usuario_existente(nome):
            raise ValueError("Já existe um usuário cadastrado com este nome.")
        
        senha_hash = hashlib.sha256(senha.encode()).hexdigest() 
        salvar_no_banco_de_dados(nome, cargo, role, senha_hash)

        return True
    except Exception as e:
        raise RuntimeError("Erro ao processar o formulário: " + str(e))

def salvar_no_banco_de_dados(nome, cargo, role, senha):
    try:
        # Insere no banco de dados
        with conexao.cursor() as cursor:
            sql = "INSERT INTO user (account, office, password, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nome, cargo, senha, role))

        # Commit para efetivar a operação no banco de dados
        conexao.commit()
        return True
    except Exception as e:
        return False