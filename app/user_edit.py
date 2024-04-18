import hashlib

from .models import conectar_db

conexao = conectar_db()

def user_edit(id_user, nome, cargo, role, senha):
    try:
        with conexao.cursor() as cursor:
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            sql = "UPDATE user SET account = %s, office = %s, role = %s, password = %s WHERE id_user = %s"
            cursor.execute(sql, (nome, cargo, role, senha_hash, id_user))

        conexao.commit()
        return True
    except Exception as e:
        return False