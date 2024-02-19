import os
from datetime import datetime
from .models import conectar_db

conexao = conectar_db()

def obter_valor_atual_location(id_pdf):
    try:
        with conexao.cursor() as cursor:
            sql = "SELECT location FROM pdf WHERE id_pdf = %s"
            cursor.execute(sql, (id_pdf))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]
            else:
                return None
    except Exception as e:
        print(f"Erro ao obter valor atual de 'location': {e}")
        return None

def pdf_edit(id_pdf, nome, categoria, data, arquivo):
    try:
        valor_atual_location = obter_valor_atual_location(id_pdf)

        caminho_arquivo = None

        if arquivo:
            diretorio = os.path.join(os.getcwd(), 'app', 'data')
            if not os.path.exists(diretorio):
                os.makedirs(diretorio)

            nome_arquivo = f"{categoria}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            caminho_arquivo = os.path.join(diretorio, nome_arquivo)
            arquivo.save(caminho_arquivo)
        else:
            caminho_arquivo = valor_atual_location

        if data:
            data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        else:
            data_formatada = None

        salvar_no_banco_de_dados(id_pdf, nome, categoria, data_formatada, caminho_arquivo)

    except Exception as e:
        print(f"Erro ao processar o formulário: {e}")

def salvar_no_banco_de_dados(id_pdf, nome, categoria, data, caminho_arquivo):
    try:
        with conexao.cursor() as cursor:
            sql = "UPDATE pdf SET name = %s, category = %s, location = %s, date = %s WHERE id_pdf = %s"
            cursor.execute(sql, (nome, categoria, caminho_arquivo, data, id_pdf))

        conexao.commit()
        print("Atualização no banco de dados bem-sucedida!")
    except Exception as e:
        print(f"Erro ao atualizar no banco de dados: {e}")