import io
import pickle
from datetime import datetime
from pdf2image import convert_from_bytes
from .models import conectar_db

conexao = conectar_db()

def processar_formulario(nome, categoria, versao, data, arquivo):
    try:
        # Gera um nome para o arquivo baseado na categoria e na data/hora atual
        conteudo_arquivo = arquivo.read()  # Lê o conteúdo do arquivo como binário
        imagens = converter_pdf_para_imagens(conteudo_arquivo)

        # Converte todas as imagens para binário e as agrupa
        imagens_binarias = [converter_imagem_para_binario(imagem) for imagem in imagens]
        imagens_agrupadas = pickle.dumps(imagens_binarias)

        # Salva no banco de dados
        salvar_no_banco_de_dados(nome, categoria, data, versao, conteudo_arquivo, imagens_agrupadas)

    except Exception as e:
        print(f"Erro ao processar o formulário: {e}")

def converter_pdf_para_imagens(conteudo_arquivo):
    # Converte o conteúdo do PDF (em bytes) para uma lista de imagens
    imagens = convert_from_bytes(conteudo_arquivo)
    return imagens

def converter_imagem_para_binario(imagem):
    # Converte a imagem para um formato binário (por exemplo, PNG)
    buf = io.BytesIO()
    imagem.save(buf, format='PNG')
    conteudo_binario = buf.getvalue()
    buf.close()
    return conteudo_binario

def salvar_no_banco_de_dados(nome, categoria, data, versao, conteudo_arquivo, imagens_agrupadas):
    try:
        # Converte a data para o formato do banco de dados
        data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')

        # Ajuste conforme sua estrutura de banco de dados
        with conexao.cursor() as cursor:
            sql = "INSERT INTO pdf (name, category, version, location, date, page_images) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (nome, categoria, versao, conteudo_arquivo, data_formatada, imagens_agrupadas))

        conexao.commit()
        print("Inserção no banco de dados bem-sucedida!")
    except Exception as e:
        print(f"Erro ao inserir no banco de dados: {e}")