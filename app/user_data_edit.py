import hashlib
import re

from .models import conectar_db

conexao = conectar_db()

def user_data_edit(nome, cargo, senha, confirma_senha):
    # Verifica se as senhas são iguais
    if senha != confirma_senha:
        return "As senhas não são iguais"
    
    # Verifica se a senha é forte o suficiente
    if not is_strong_password(senha):
        return "A senha deve conter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais."
    
    try:
        with conexao.cursor() as cursor:
            senha_md5 = hashlib.md5(senha.encode()).hexdigest()
            # Evita injeção de SQL usando placeholders na consulta SQL
            sql = "UPDATE user SET office = %s, password = %s WHERE account = %s"
            cursor.execute(sql, (cargo, senha_md5, nome))
        conexao.commit()
        return "Sucesso ao atualizar"
    except Exception as e:
        return f"Erro ao atualizar: {e}"

def is_strong_password(password):
    # Verifica se a senha tem pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*()-_=+{};:,<.>]", password):
        return False
    return True