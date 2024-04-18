from .models import conectar_db

conexao = conectar_db()


def user_delete(id_user):
    try:
        # Crie um cursor para executar consultas SQL
        cursor = conexao.cursor()

        # Crie a consulta SQL para excluir o registro com base no id_pdf
        sql = "DELETE FROM user WHERE id_user = %s"
        cursor.execute(sql, (id_user,))

        # Faça o commit para efetivar a exclusão
        conexao.commit()

        # Feche o cursor
        cursor.close()

        return True

    except Exception as e:
       return False

