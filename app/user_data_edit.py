import hashlib

from .models import conectar_db

conexao = conectar_db()

def user_data_edit(nome, cargo, senha, confirma_senha):
    # Verifica se as senhas são iguais - removido
    # Verifica se a senha é forte o suficiente - removido
    
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