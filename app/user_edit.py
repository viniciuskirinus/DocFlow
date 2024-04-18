import hashlib

from .models import conectar_db

conexao = conectar_db()

def user_edit(id_user, nome, cargo, role, senha):
    try:
        with conexao.cursor() as cursor:
            # Verifica se a senha já está em MD5
            if not is_md5(senha):
                # Se não estiver em MD5, converte para MD5
                senha_md5 = hashlib.md5(senha.encode()).hexdigest()
            else:
                # Se já estiver em MD5, mantém como está
                senha_md5 = senha
            
            sql = "UPDATE user SET account = %s, office = %s, role = %s, password = %s WHERE id_user = %s"
            cursor.execute(sql, (nome, cargo, role, senha_md5, id_user))

        conexao.commit()
        return True
    except Exception as e:
        return False

def is_md5(s):
    # Verifica se a string tem 32 caracteres e é hexadecimal
    return len(s) == 32 and all(c in '0123456789abcdef' for c in s)
