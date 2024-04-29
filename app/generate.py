import io
import pickle
import boto3
from datetime import datetime
from pdf2image import convert_from_bytes
from .models import conectar_db
import os
import pymysql.cursors


conexao = conectar_db()



def processar_formulario(nome, categoria, versao, data, setor, arquivo):
    try:
        if verificar_documento_existente(nome):
            return False  # Documento já existe, portanto, retorno False
        
        conteudo_arquivo = arquivo.read()
        imagens = convert_from_bytes(conteudo_arquivo)
        imagens_binarias = [converter_imagem_para_binario(imagem) for imagem in imagens]
        imagens_agrupadas = pickle.dumps(imagens_binarias)

        # Salva no banco de dados
        if not salvar_no_banco_de_dados(nome, categoria, setor, data, versao, conteudo_arquivo, imagens_agrupadas):
            raise RuntimeError("Falha ao salvar no banco de dados")

        criar_pasta_s3(nome)
        fazer_upload_para_s3(nome, versao, conteudo_arquivo)

        criar_e_enviar_notificacao()
        
        return True
    except Exception as e:
        raise RuntimeError("Erro ao processar o formulário: " + str(e))

def verificar_documento_existente(nome):
    try:
        with conexao.cursor() as cursor:
            sql_verificar = "SELECT name FROM pdf WHERE name = %s"
            cursor.execute(sql_verificar, (nome,))
            resultado = cursor.fetchone()
            if resultado is not None:  # Se a consulta retornar algum resultado
                return True  # Documento existe
            else:
                return False  # Documento não existe
    except Exception as e:
        # Se ocorrer um erro durante a execução da consulta, relança a exceção
        raise RuntimeError("Erro ao verificar a existência do documento: " + str(e))

def criar_e_enviar_notificacao():
    try:
        ultimo_id_inserido = obter_ultimo_id_inserido()
        descricao = "Novo documento lançado no portal"
        hora_atual = datetime.now()
        if not enviar_notificacao(descricao, hora_atual, ultimo_id_inserido):
            raise RuntimeError("Falha ao enviar a notificação")
    except Exception as e:
        raise RuntimeError("Erro ao criar e enviar notificação: " + str(e))

def obter_ultimo_id_inserido():
    try:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT LAST_INSERT_ID()")
            ultimo_id_inserido = cursor.fetchone()[0]
            return ultimo_id_inserido
    except Exception as e:
        raise RuntimeError("Erro ao obter o último ID inserido: " + str(e))

def enviar_notificacao(descricao, hora, ultimo_id_inserido):
    try:
        with conexao.cursor(pymysql.cursors.DictCursor) as cursor:  # Usando DictCursor
            # Inicia uma transação
            conexao.begin()

            # Insere a nova notificação
            sql_inserir_notificacao = "INSERT INTO notifications (description, time, id_pdf) VALUES (%s, %s, %s)"
            cursor.execute(sql_inserir_notificacao, (descricao, hora, ultimo_id_inserido))

            # Obtém o ID da notificação que acabou de ser inserida
            id_notificacao = cursor.lastrowid

            # Busca todos os usuários com a role 'user'
            sql_buscar_usuarios = "SELECT id_user FROM user WHERE role = 'user'"
            cursor.execute(sql_buscar_usuarios)
            usuarios = cursor.fetchall()  # Agora retorna uma lista de dicionários

            # Para cada usuário, insere uma entrada na tabela user_notifications
            sql_inserir_user_notification = "INSERT INTO user_notifications (id_user, id_notifications, `read`) VALUES (%s, %s, %s)"
            for usuario in usuarios:
                cursor.execute(sql_inserir_user_notification, (usuario['id_user'], id_notificacao, False))

            # Se todas as operações foram bem sucedidas, commit a transação
            conexao.commit()
            return True

    except Exception as e:
        # Se houver erro, reverte todas as operações feitas durante a transação
        conexao.rollback()
        # Levanta uma exceção com mensagem de erro
        raise RuntimeError("Erro ao enviar notificação: " + str(e))

def converter_imagem_para_binario(imagem):
    buf = io.BytesIO()
    imagem.save(buf, format='PNG')
    conteudo_binario = buf.getvalue()
    buf.close()
    return conteudo_binario

def salvar_no_banco_de_dados(nome, categoria, setor, data, versao, conteudo_arquivo, imagens_agrupadas):
    try:
        data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        with conexao.cursor() as cursor:
            sql_inserir = "INSERT INTO pdf (name, category, sector, version, location, date, page_images) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_inserir, (nome, categoria, setor, versao, conteudo_arquivo, data_formatada, imagens_agrupadas))
        conexao.commit()
        return True
    except Exception as e:
        return False

def criar_pasta_s3(nome):
    bucket_name = os.getenv("BUCKET_NAME")
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                             aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))
    s3_client.put_object(Bucket=bucket_name, Key=f'Documents/{nome}/')

def fazer_upload_para_s3(nome, versao, conteudo_arquivo):
    bucket_name = os.getenv("BUCKET_NAME")
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                             aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))
    key = f'Documents/{nome}/{nome}_{versao}.pdf'
    s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=conteudo_arquivo,
        ContentType='application/pdf'  
    )
