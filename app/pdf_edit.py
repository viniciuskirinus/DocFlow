import io
import pickle
from datetime import datetime
from pdf2image import convert_from_bytes
import boto3
import os
from .models import conectar_db
import pymysql.cursors


conexao = conectar_db()

def obter_valores_atuais(id_pdf):
    try:
        with conexao.cursor() as cursor:
            sql = "SELECT name, location, page_images FROM pdf WHERE id_pdf = %s"
            cursor.execute(sql, (id_pdf,))
            resultado = cursor.fetchone()
            if resultado:
                return resultado
            else:
                return None, None, None
    except Exception as e:
        print(f"Erro ao obter valores atuais: {e}")
        return None, None, None

def renomear_pasta_s3(nome_antigo, nome_novo):
    # Recuperar o nome do bucket das variáveis de ambiente
    bucket_name = os.getenv("BUCKET_NAME")

    s3_client = boto3.client('s3',
                             aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                             aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))

    # Verifica se a pasta com o nome antigo existe
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=f'Documents/{nome_antigo}/')

    if 'Contents' in response:
        # Renomeia a pasta para o novo nome
        for obj in response['Contents']:
            novo_key = obj['Key'].replace(nome_antigo, nome_novo, 1)
            s3_client.copy_object(Bucket=bucket_name, CopySource=f"{bucket_name}/{obj['Key']}", Key=novo_key)
            s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])

def fazer_upload_para_s3(nome, version, conteudo_arquivo):
    if conteudo_arquivo:
        # Recuperar o nome do bucket das variáveis de ambiente
        bucket_name = os.getenv("BUCKET_NAME")
        
        s3_client = boto3.client('s3',
                                 aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                                 aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))
        key = f'Documents/{nome}/{nome}_{version}.pdf'
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=conteudo_arquivo,
            ContentType='application/pdf'  # Adicionando o ContentType
        )

def converter_pdf_para_imagens(conteudo_arquivo):
    imagens = convert_from_bytes(conteudo_arquivo)
    return imagens

def converter_imagem_para_binario(imagem):
    buf = io.BytesIO()
    imagem.save(buf, format='PNG')
    conteudo_binario = buf.getvalue()
    buf.close()
    return conteudo_binario

def pdf_edit(id_pdf, nome, categoria, setor, version, data, arquivo):
    try:
        valor_atual_nome, valor_atual_location, valor_atual_page_images = obter_valores_atuais(id_pdf)

        if nome != valor_atual_nome:
            # Se o nome do documento foi alterado, renomeia a pasta no S3
            renomear_pasta_s3(valor_atual_nome, nome)

        if arquivo:
            conteudo_arquivo = arquivo.read()  # Lê o conteúdo do arquivo como binário
            imagens = converter_pdf_para_imagens(conteudo_arquivo)
            imagens_binarias = [converter_imagem_para_binario(imagem) for imagem in imagens]
            imagens_agrupadas = pickle.dumps(imagens_binarias)
            
            # Faz o upload do novo arquivo para o S3
            fazer_upload_para_s3(nome, version, conteudo_arquivo)
        else:
            # Mantém os valores atuais se um novo arquivo não for enviado
            conteudo_arquivo = valor_atual_location
            imagens_agrupadas = valor_atual_page_images

        if data:
            data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        else:
            data_formatada = None

        # Atualiza o registro no banco de dados
        salvar_no_banco_de_dados(id_pdf, nome, categoria, setor, version, data_formatada, conteudo_arquivo, imagens_agrupadas)

        criar_e_enviar_notificacao(id_pdf)

        return True
    except Exception as e:
        return False

def salvar_no_banco_de_dados(id_pdf, nome, categoria, setor, version, data, conteudo_arquivo, imagens_agrupadas):
    try:
        with conexao.cursor() as cursor:
            sql = "UPDATE pdf SET name = %s, category = %s, sector = %s, version = %s, location = %s, date = %s, page_images = %s WHERE id_pdf = %s"
            cursor.execute(sql, (nome, categoria, setor, version, conteudo_arquivo, data, imagens_agrupadas, id_pdf))

        conexao.commit()
        return True
    except Exception as e:
        return False

def criar_e_enviar_notificacao(id_pdf):
    try:
        ultimo_id_inserido = id_pdf
        descricao = "Nova versão lançada no portal"
        hora_atual = datetime.now()
        if not enviar_notificacao(descricao, hora_atual, ultimo_id_inserido):
            raise RuntimeError("Falha ao enviar a notificação")
    except Exception as e:
        raise RuntimeError("Erro ao criar e enviar notificação: " + str(e))

def enviar_notificacao(descricao, hora_atual, ultimo_id_inserido):
    try:
        with conexao.cursor(pymysql.cursors.DictCursor) as cursor:  # Usando DictCursor
            # Inicia uma transação
            conexao.begin()

            # Insere a nova notificação
            sql_inserir_notificacao = "INSERT INTO notifications (description, time, id_pdf) VALUES (%s, %s, %s)"
            cursor.execute(sql_inserir_notificacao, (descricao, hora_atual, ultimo_id_inserido))

            # Busca todos os usuários com a role 'user'
            sql_buscar_usuarios = "SELECT id_user FROM user WHERE role = 'user'"
            cursor.execute(sql_buscar_usuarios)
            usuarios = cursor.fetchall()  # Agora retorna uma lista de dicionários

            # Para cada usuário, insere uma entrada na tabela user_notifications
            sql_inserir_user_notification = "INSERT INTO user_notifications (id_user, id_notifications, `read`) VALUES (%s, %s, %s)"
            for usuario in usuarios:
                cursor.execute(sql_inserir_user_notification, (usuario['id_user'], ultimo_id_inserido, False))

            # Se todas as operações foram bem sucedidas, commit a transação
            conexao.commit()
            return True

    except Exception as e:
        # Se houver erro, reverte todas as operações feitas durante a transação
        conexao.rollback()
        # Levanta uma exceção com mensagem de erro
        raise RuntimeError("Erro ao enviar notificação: " + str(e))