import io
import pickle
from datetime import datetime
from pdf2image import convert_from_bytes
from .models import conectar_db

conexao = conectar_db()

def obter_valores_atuais(id_pdf):
    try:
        with conexao.cursor() as cursor:
            sql = "SELECT location, page_images FROM pdf WHERE id_pdf = %s"
            cursor.execute(sql, (id_pdf,))
            resultado = cursor.fetchone()
            if resultado:
                return resultado
            else:
                return None, None
    except Exception as e:
        print(f"Erro ao obter valores atuais: {e}")
        return None, None

def converter_pdf_para_imagens(conteudo_arquivo):
    imagens = convert_from_bytes(conteudo_arquivo)
    return imagens

def converter_imagem_para_binario(imagem):
    buf = io.BytesIO()
    imagem.save(buf, format='PNG')
    conteudo_binario = buf.getvalue()
    buf.close()
    return conteudo_binario

def pdf_edit(id_pdf, nome, categoria, data, arquivo):
    try:
        valor_atual_location, valor_atual_page_images = obter_valores_atuais(id_pdf)

        if arquivo:
            conteudo_arquivo = arquivo.read()  # Lê o conteúdo do arquivo como binário
            imagens = converter_pdf_para_imagens(conteudo_arquivo)
            imagens_binarias = [converter_imagem_para_binario(imagem) for imagem in imagens]
            imagens_agrupadas = pickle.dumps(imagens_binarias)
        else:
            # Mantém os valores atuais se um novo arquivo não for enviado
            conteudo_arquivo = valor_atual_location
            imagens_agrupadas = valor_atual_page_images

        if data:
            data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        else:
            data_formatada = None

        # Atualiza o registro no banco de dados
        salvar_no_banco_de_dados(id_pdf, nome, categoria, data_formatada, conteudo_arquivo, imagens_agrupadas)

    except Exception as e:
        print(f"Erro ao processar o formulário: {e}")

def salvar_no_banco_de_dados(id_pdf, nome, categoria, data, conteudo_arquivo, imagens_agrupadas):
    try:
        with conexao.cursor() as cursor:
            sql = "UPDATE pdf SET name = %s, category = %s, location = %s, date = %s, page_images = %s WHERE id_pdf = %s"
            cursor.execute(sql, (nome, categoria, conteudo_arquivo, data, imagens_agrupadas, id_pdf))

        conexao.commit()
        print("Atualização no banco de dados bem-sucedida!")
    except Exception as e:
        print(f"Erro ao atualizar no banco de dados: {e}")
