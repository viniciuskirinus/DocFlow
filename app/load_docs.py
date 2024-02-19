from flask import Flask
from .models import conectar_db

app = Flask(__name__)

# Função para obter dados do banco de dados com base na categoria
def obter_dados_do_banco_por_categoria(categoria):
    # Substitua "sua_query_sql" pela sua consulta SQL para obter os dados desejados
    query = f"SELECT id_pdf, name, location, date, category FROM pdf WHERE category = '{categoria}'"
    
    # Obtém a conexão com o banco de dados
    conexao = conectar_db()
    cursor = conexao.cursor()

    # Executa a consulta
    cursor.execute(query)

    # Obtém os resultados e colunas
    resultados = cursor.fetchall()
    colunas = [col[0] for col in cursor.description]

    # Fecha a conexão com o banco de dados
    cursor.close()
    conexao.close()

    # Monta a lista de dicionários
    dados = [dict(zip(colunas, row)) for row in resultados]

    return dados