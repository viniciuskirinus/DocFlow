from .models import conectar_db

conexao = conectar_db()


def pdf_delete(id_pdf):
    try:
        # Crie um cursor para executar consultas SQL
        cursor = conexao.cursor()

        # Crie a consulta SQL para excluir o registro com base no id_pdf
        sql = "DELETE FROM pdf WHERE id_pdf = %s"
        cursor.execute(sql, (id_pdf,))

        # Faça o commit para efetivar a exclusão
        conexao.commit()

        # Feche o cursor
        cursor.close()

        print("Exclusão no banco de dados bem-sucedida!")

    except Exception as e:
        print(f"Erro ao excluir do banco de dados: {e}")
