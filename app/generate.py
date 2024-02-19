import os
from datetime import datetime
from .models import conectar_db

conexao = conectar_db()

def processar_formulario(nome, categoria, data, arquivo):
    try:
        # Cria o diretório se não existir
        diretorio = os.path.join(os.getcwd(), 'app', 'data')
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)

        # Extrai informações do arquivo
        nome_arquivo = f"{categoria}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        caminho_arquivo = os.path.join(diretorio, nome_arquivo)

        # Salva o arquivo na pasta
        arquivo.save(caminho_arquivo)

        # Faça o processamento necessário com os dados
        print(f"Nome: {nome}, Categoria: {categoria}, Data: {data}, Arquivo: {caminho_arquivo}")

        # Salva no banco de dados
        salvar_no_banco_de_dados(nome, categoria, data, nome_arquivo)

    except Exception as e:
        print(f"Erro ao processar o formulário: {e}")

def salvar_no_banco_de_dados(nome, categoria, data, nome_arquivo):
    try:
        # Converte a data para o formato do banco de dados
        data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')

        # Insere no banco de dados
        with conexao.cursor() as cursor:
            sql = "INSERT INTO pdf (name, category, location, date) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nome, categoria, nome_arquivo, data_formatada))


        # Commit para efetivar a operação no banco de dados
        conexao.commit()
        print("Inserção no banco de dados bem-sucedida!")
    except Exception as e:
        print(f"Erro ao inserir no banco de dados: {e}")
