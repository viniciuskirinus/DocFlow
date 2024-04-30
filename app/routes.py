from flask import Flask, Blueprint, render_template, flash, redirect, url_for, session, request, jsonify, make_response
import os
import pickle
from .forms import processar_login
from .generate import processar_formulario, verificar_documento_existente
from .pdf_edit import pdf_edit, criar_e_enviar_notificacao
from .pdf_delete import pdf_delete
from .user_delete import user_delete
from .user_edit import user_edit
from .user_data_edit import user_data_edit
from .load_docs import obter_dados_do_banco_por_categoria
from .load_docs_admin import obter_dados_lista_pdf
from .load_users_admin import obter_dados_lista_user
from .generateuser import processar_formulario_user, verificar_usuario_existente
from .process_chat import process_message
from base64 import b64encode
from .models import conectar_db
from .s3_database import list_folders_and_files
from .send_s3 import send_s3
from .notifications import get_notifications
from .read_notifications import marcar_todas_como_lidas


#carrega as chaves da api do gpt e huggingface para processar o chat
openai_api_key = os.getenv("OPENAI_API_KEY")
huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

#rota de inicio
login_routes = Blueprint('login', __name__, template_folder='templates')

#rota de inicio administrador
admin_routes = Blueprint('admin', __name__, template_folder='templates')
#rota de gerenciamento pdf
admin_pdf_generate_routes = Blueprint('generate', __name__, template_folder='templates')
admin_pdf_routes = Blueprint('pdf', __name__, template_folder='templates')
admin_pdf_edit_routes = Blueprint('edit', __name__, template_folder='templates')
admin_pdf_delete_routes = Blueprint('delete', __name__, template_folder='templates')
#rota de gerenciamento de usuarios
admin_user_routes = Blueprint('usuarios', __name__, template_folder='templates')
admin_user_generate_routes = Blueprint('generateuser', __name__, template_folder='templates')
admin_user_delete_routes = Blueprint('deleteuser', __name__, template_folder='templates')
admin_user_edit_routes = Blueprint('edituser', __name__, template_folder='templates')

#rota de arquivos antigos
admin_old_files_routes = Blueprint('old_files', __name__, template_folder='templates')

#rota de envio arquivos s3
admin_old_files_send_routes = Blueprint('send_files', __name__, template_folder='templates')

#rota para exibicao do pdf
user_show_pdf_routes = Blueprint('showpdf', __name__, template_folder='templates')

#rota de inicio usuario
home_routes = Blueprint('home', __name__, template_folder='templates')

#rota de categorias
user_procedimentos_routes = Blueprint('user_procedimentos', __name__, template_folder='templates')
user_manuais_routes = Blueprint('user_manuais', __name__, template_folder='templates')
user_instrucoes_routes = Blueprint('user_instrucoes', __name__, template_folder='templates')
user_iso_routes = Blueprint('user_iso', __name__, template_folder='templates')
user_documentos_gerais_routes = Blueprint('user_documentos_gerais', __name__, template_folder='templates')
user_projetos_routes = Blueprint('user_projetos', __name__, template_folder='templates')
user_documentos_clientes_routes = Blueprint('user_documentos_clientes', __name__, template_folder='templates')
user_politicas_gerais_routes = Blueprint('user_politicas_gerais', __name__, template_folder='templates')

#edicao dados usuario
user_edit_data_routes = Blueprint('edit_data', __name__, template_folder='templates')

#rota processa chat
process_chat_routes = Blueprint('process_chat', __name__, template_folder='templates')

#rota de logout
logout_routes = Blueprint('logout', __name__, template_folder='templates')

#marcando notificações como lidas
marcar_todas_como_lidas_routes = Blueprint('marcar_todas_como_lidas', __name__, template_folder='templates')

@login_routes.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Falha no login: por favor, preencha ambos os campos.', 'error')
        else:
            resultado_autenticacao = processar_login(username, password)
            flash(resultado_autenticacao, 'info')
            if resultado_autenticacao == "Login bem-sucedido!":
                if 'role' in session and session['role'] == "admin":
                    return redirect(url_for('admin.admin'))
                elif 'role' in session and session['role'] == "user":
                    return redirect(url_for('home.home'))

    return render_template('login.html')

@admin_routes.route('/admin')
def admin():
    # Verifique se o usuário está autenticado e possui a função de administrador
    if 'username' in session and 'role' in session and session['role'] == "admin":
        return render_template('admin.html', active_page='admin.admin') 
    else:
        # Se não estiver autenticado como administrador, redirecione para a página de login
        return redirect(url_for('login.login'))

@home_routes.route('/home')
def home():
    if 'username' in session and 'role' in session and session['role'] == "user":
        # Obtenha a mensagem de alerta da sessão
        alert_message = session.pop('alert_message', None)
        notifications = get_notifications()

        return render_template('home.html', active_page='home.home', alert_message=alert_message, notifications=notifications) 
    else:
        return redirect(url_for('login.login'))

@user_procedimentos_routes.route('/user_procedimentos')
def userprocedimentos():
    if 'username' in session and 'role' in session and session['role'] == "user":
        categoria = 'Procedimentos'  # Defina a categoria desejada
        dados_do_banco = obter_dados_do_banco_por_categoria(categoria)
        notifications = get_notifications()
        return render_template('user_procedimentos.html', active_page='user_procedimentos.userprocedimentos', dados=dados_do_banco, notifications=notifications) 
    else:
        return redirect(url_for('login.login'))
    
@user_manuais_routes.route('/user_manuais')
def usermanuais():
    if 'username' in session and 'role' in session and session['role'] == "user":
        categoria = 'Manuais'  # Defina a categoria desejada
        dados_do_banco = obter_dados_do_banco_por_categoria(categoria)
        notifications = get_notifications()
        return render_template('user_manuais.html', active_page='user_manuais.usermanuais', dados=dados_do_banco, notifications=notifications) 
    else:
        return redirect(url_for('login.login'))

@user_instrucoes_routes.route('/user_instrucoes')
def userinstrucoes():
    if 'username' in session and 'role' in session and session['role'] == "user":
        categoria = 'Instrucoes'  # Defina a categoria desejada
        dados_do_banco = obter_dados_do_banco_por_categoria(categoria)
        notifications = get_notifications()
        return render_template('user_instrucoes.html', active_page='user_instrucoes.userinstrucoes', dados=dados_do_banco, notifications=notifications) 
    else:
        return redirect(url_for('login.login'))

@user_iso_routes.route('/user_iso')
def useriso():
    if 'username' in session and 'role' in session and session['role'] == "user":
        categoria = 'ISO'  # Defina a categoria desejada
        dados_do_banco = obter_dados_do_banco_por_categoria(categoria)
        notifications = get_notifications()
        return render_template('user_iso.html', active_page='user_iso.useriso', dados=dados_do_banco, notifications=notifications) 
    else:
        return redirect(url_for('login.login'))

@user_documentos_gerais_routes.route('/user_documentos_gerais')
def userdocumentosgerais():
    if 'username' in session and 'role' in session and session['role'] == "user":
        categoria = 'Documentos Gerais'  # Defina a categoria desejada
        dados_do_banco = obter_dados_do_banco_por_categoria(categoria)
        notifications = get_notifications()
        return render_template('user_documentos_gerais.html', active_page='user_documentos_gerais.userdocumentosgerais', dados=dados_do_banco, notifications=notifications) 
    else:
        return redirect(url_for('login.login'))
    
@user_projetos_routes.route('/user_projetos')
def userprojetos():
    if 'username' in session and 'role' in session and session['role'] == "user":
        categoria = 'Projetos'  # Defina a categoria desejada
        dados_do_banco = obter_dados_do_banco_por_categoria(categoria)
        notifications = get_notifications()
        return render_template('user_projetos.html', active_page='user_projetos.userprojetos', dados=dados_do_banco, notifications=notifications) 
    else:
        return redirect(url_for('login.login'))
    
@user_documentos_clientes_routes.route('/user_documentos_clientes')
def userdocumentos_clientes():
    if 'username' in session and 'role' in session and session['role'] == "user":
        categoria = 'Documentos de Clientes'  # Defina a categoria desejada
        dados_do_banco = obter_dados_do_banco_por_categoria(categoria)
        notifications = get_notifications()
        return render_template('user_documentos_clientes.html', active_page='user_documentos_clientes.userdocumentos_clientes', dados=dados_do_banco, notifications=notifications) 
    else:
        return redirect(url_for('login.login'))
    
@user_politicas_gerais_routes.route('/user_politicas_gerais')
def userpoliticas_gerais():
    if 'username' in session and 'role' in session and session['role'] == "user":
        categoria = 'Politicas Gerais'  # Defina a categoria desejada
        dados_do_banco = obter_dados_do_banco_por_categoria(categoria)
        notifications = get_notifications()
        return render_template('user_politicas_gerais.html', active_page='user_politicas_gerais.userpoliticas_gerais', dados=dados_do_banco, notifications=notifications) 
    else:
        return redirect(url_for('login.login'))
    
@user_show_pdf_routes.route('/showpdf', methods=['POST'])
def showpdf_route():
    data = request.json
    pdf_id = data.get('pdf_id')

    if pdf_id is not None:
        conexao = conectar_db()
        cursor = conexao.cursor()
        cursor.execute("SELECT page_images FROM pdf WHERE id_pdf = %s", (pdf_id,))
        result = cursor.fetchone()

        if result is None:
            return jsonify({'error': 'PDF não encontrado no banco de dados.'}), 404

        # Deserializa o blob (assegure-se de que os dados sejam seguros antes de fazer isso)
        pdf_blobs = pickle.loads(result[0])
        pdf_images_base64 = [b64encode(blob).decode('utf-8') for blob in pdf_blobs]

        return jsonify({'pdf_images_base64': pdf_images_base64}), 200
    else:
        return jsonify({'error': 'ID do PDF não fornecido.'}), 400

@process_chat_routes.route('/process_chat', methods=['POST'])
def chat_endpoint():
    data = request.json
    user_message = data.get('message')
    pdf_id = data.get('pdfid')
    response = process_message(user_message, pdf_id)
    return jsonify({'response': response})

@admin_pdf_routes.route('/pdf')
def pdf():
    if 'username' in session and 'role' in session and session['role'] == "admin":
        dados_do_banco = obter_dados_lista_pdf()
        return render_template('pdf.html', active_page='pdf.pdf', dados=dados_do_banco) 
    else:
        return redirect(url_for('login.login'))
    
@admin_old_files_routes.route('/old_files')
def old_files():
    if 'username' in session and 'role' in session and session['role'] == "admin":
        # Obter lista de pastas e arquivos dentro da pasta 'Documents/'
        bucket_name = os.getenv("BUCKET_NAME")
        folder_name = 'Documents/'
        folders, files = list_folders_and_files(bucket_name, folder_name)


        # Renderizar o template HTML existente e passar as listas como contexto
        return render_template('old_files.html', active_page='old_files.old_files', folders=folders, files=files)
    else:
        return redirect(url_for('login.login'))
    
@admin_old_files_send_routes.route('/send_files', methods=['POST'])
def send_files():
    if 'username' in session and 'role' in session and session['role'] == "admin":
        # Obter dados do formulário
        folder = request.form.get('folder')

        # Verificar se há arquivos enviados
        if 'files[]' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400

        files = request.files.getlist('files[]')  # Obter uma lista de arquivos enviados
        file_names = [file.filename for file in files]  # Obter uma lista de nomes de arquivos

        # Chamar a função send_s3 com os argumentos corretos
        send_s3(folder, files, file_names)

        return jsonify({'redirect': url_for('old_files.old_files')})
    else:
        return redirect(url_for('login.login'))

@admin_pdf_edit_routes.route('/edit', methods=['POST'])
def edit():
    if 'username' in session and 'role' in session and session['role'] == "admin":
        id_pdf = request.form.get('edit_id_pdf')  
        nome = request.form.get('edit_nome')       
        categoria = request.form.get('edit_categoria')
        setor = request.form.get('edit_setor')
        version = request.form.get('edit_version') 
        data = request.form.get('edit_data')   
        arquivo = request.files['arquivo']

        try:
            print("Editando PDF...")
            pdf_edit(id_pdf, nome, categoria, setor, version, data, arquivo)
            
            print("Enviando notificação...")
            criar_e_enviar_notificacao(id_pdf)
            
            print("Notificação enviada com sucesso!")
            return jsonify(success=True)  # Retorna uma resposta indicando sucesso
        except Exception as e:
            print("Erro ao editar ou enviar notificação:", str(e))
            return jsonify(success=False, error=str(e))  # Retorna uma resposta indicando erro
    else:
        return jsonify(success=False, error="Unauthorized"), 401  # Retorna uma resposta de não autorizado
 
@admin_pdf_delete_routes.route('/delete', methods=['POST'])
def delete():
    if 'username' in session and 'role' in session and session['role'] == "admin":
        id_pdf = request.form.get('delete_id_pdf')

        try:
            pdf_delete(id_pdf)
            return jsonify(success=True)  # Retorna uma resposta indicando sucesso
        except Exception as e:
            return jsonify(success=False, error=str(e))  # Retorna uma resposta indicando erro
    else:
        return jsonify(success=False, error="Unauthorized"), 401  # Retorna uma resposta de não autorizado

@admin_pdf_generate_routes.route('/generate', methods=['POST'])
def generate():
    try:
        if 'username' not in session or 'role' not in session or session['role'] != "admin":
            return jsonify(success=False, error="Unauthorized"), 401

        nome = request.form.get('nome')

        if verificar_documento_existente(nome):
            return jsonify(success=False, error="Já existe um documento cadastrado com este nome."), 400

        categoria = request.form.get('categoria')
        versao = request.form.get('versao')
        data = request.form.get('data')
        setor = request.form.get('setor')
        arquivo = request.files['arquivo'] if 'arquivo' in request.files else None

        sucesso = processar_formulario(nome, categoria, versao, data, setor, arquivo)
        
        if sucesso:
            return jsonify(success=True)  # Retorna uma resposta indicando sucesso
        else:
            return jsonify(success=False, error="Erro ao processar o formulário: Documento já existe."), 400  # Retorna uma resposta de erro indicando que o documento já existe
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500  # Retorna uma resposta de erro com a mensagem de exceção

@admin_user_routes.route('/users')
def usuarios():
    if 'username' in session and 'role' in session and session['role'] == "admin":
        dados_do_banco = obter_dados_lista_user()
        return render_template('usuarios.html', active_page='usuarios.usuarios', dados=dados_do_banco) 
    else:
        return redirect(url_for('login.login'))
    
@admin_user_generate_routes.route('/generateuser', methods=['POST'])
def generateuser():
    if 'username' in session and 'role' in session and session['role'] == "admin":
        # Obter dados do formulário
        nome = request.form.get('nome')
        cargo = request.form.get('cargo')
        role = request.form.get('role')
        senha = request.form.get('senha')
        try:
            # Verificar se já existe um usuário com o mesmo nome
            if verificar_usuario_existente(nome):
                return jsonify(success=False, error="Já existe um usuário cadastrado com este nome."), 400
            
            sucesso = processar_formulario_user(nome, cargo, role, senha)

            if sucesso:
                    return jsonify(success=True)  # Retorna uma resposta indicando sucesso
            else:
                return jsonify(success=False, error="Erro ao processar o formulário."), 500  # Retorna uma resposta de erro genérica
        except Exception as e:
            return jsonify(success=False, error=str(e)), 500  # Retorna uma resposta de erro com a mensagem de exceção
    else:
        unauthorized_response = make_response(jsonify(success=False, error="Unauthorized"), 401)
        unauthorized_response.headers['Content-Type'] = 'application/json'
        return unauthorized_response
    
@admin_user_edit_routes.route('/edituser', methods=['POST'])
def edituser():
    if 'username' in session and 'role' in session and session['role'] == "admin":
        id_user = request.form.get('edit_id_user')  
        nome = request.form.get('edit_nome')
        cargo = request.form.get('edit_cargo')
        role = request.form.get('edit_role')
        senha = request.form.get('edit_senha')
        try:
            user_edit(id_user, nome, cargo, role, senha)
        
            return jsonify(success=True)  # Retorna uma resposta indicando sucesso
        except Exception as e:
            return jsonify(success=False, error=str(e))  # Retorna uma resposta indicando erro
    else:
        return jsonify(success=False, error="Unauthorized"), 401  # Retorna uma resposta de não autorizado
    
@admin_user_delete_routes.route('/deleteuser', methods=['POST'])
def deleteuser():
    if 'username' in session and 'role' in session and session['role'] == "admin":
        id_user = request.form.get('delete_id_user') 
        try: 
            user_delete(id_user)
            
            return jsonify(success=True)  # Retorna uma resposta indicando sucesso
        except Exception as e:
            return jsonify(success=False, error=str(e))  # Retorna uma resposta indicando erro
    else:
        return jsonify(success=False, error="Unauthorized"), 401  # Retorna uma resposta de não autorizado
    

@user_edit_data_routes.route('/edit_data', methods=['POST'])
def edit_data():
    if 'username' in session and 'role' in session and session['role'] == "user":
        # Obter dados do formulário
        nome = request.form.get('name')
        cargo = request.form.get('office')
        senha = request.form.get('password')
        
        # Chamar a função user_data_edit e capturar o retorno
        retorno = user_data_edit(nome, cargo, senha)
        
        # Defina uma mensagem de alerta com base no retorno
        if "Sucesso" in retorno:
            session['alert_message'] = (retorno, 'success')
        else:
            session['alert_message'] = (retorno, 'error')
        
        # Redirecionar para a página inicial
        return redirect(url_for('home.home'))
    else:
        return redirect(url_for('login.login'))
    
@marcar_todas_como_lidas_routes.route('/marcar_todas_como_lidas')
def marcar_todas_como_lidas_route():
    return marcar_todas_como_lidas()

@logout_routes.route('/logout')
def logout():
    try:
        conexao = conectar_db()
        # Limpar todas as transações pendentes
        conexao.rollback()

        # Fechar a conexão com o banco de dados
        conexao.close()

        # Limpar a sessão
        session.clear()

        # Redirecionar para a página de login
        return redirect(url_for('login.login'))
    except Exception as e:
        # Log de qualquer exceção que ocorra durante o logout
        print("Erro durante o logout:", e)
        # Se ocorrer um erro, você pode querer redirecionar para uma página de erro
        return redirect(url_for('login.login'))
