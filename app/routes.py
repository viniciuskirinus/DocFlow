from flask import Blueprint, render_template, flash, redirect, url_for, session, request, send_from_directory, jsonify, request
import os
from flask import Flask
import pickle
from .forms import processar_login
from .generate import processar_formulario
from .pdf_edit import pdf_edit
from .pdf_delete import pdf_delete
from .user_delete import user_delete
from .user_edit import user_edit
from .load_docs import obter_dados_do_banco_por_categoria
from .load_docs_admin import obter_dados_lista_pdf
from .load_users_admin import obter_dados_lista_user
from .generateuser import processar_formulario_user
from .process_chat import process_message
from base64 import b64encode
from .models import conectar_db

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


#rota processa chat
process_chat_routes = Blueprint('process_chat', __name__, template_folder='templates')

#rota de logout
logout_routes = Blueprint('logout', __name__, template_folder='templates')


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
        return render_template('home.html', active_page='home.home') 
    else:
        return redirect(url_for('login.login'))

@user_procedimentos_routes.route('/user_procedimentos')
def userprocedimentos():
    if 'username' in session and 'role' in session and session['role'] == "user":
        categoria = 'Procedimentos'  # Defina a categoria desejada
        dados_do_banco = obter_dados_do_banco_por_categoria(categoria)
        return render_template('user_procedimentos.html', active_page='user_procedimentos.userprocedimentos', dados=dados_do_banco) 
    else:
        return redirect(url_for('login.login'))
    
@user_manuais_routes.route('/user_manuais')
def usermanuais():
    if 'username' in session and 'role' in session and session['role'] == "user":
        categoria = 'Manuais'  # Defina a categoria desejada
        dados_do_banco = obter_dados_do_banco_por_categoria(categoria)
        return render_template('user_manuais.html', active_page='user_manuais.usermanuais', dados=dados_do_banco) 
    else:
        return redirect(url_for('login.login'))

@user_instrucoes_routes.route('/user_instrucoes')
def userinstrucoes():
    if 'username' in session and 'role' in session and session['role'] == "user":
        categoria = 'Instrucoes'  # Defina a categoria desejada
        dados_do_banco = obter_dados_do_banco_por_categoria(categoria)
        return render_template('user_instrucoes.html', active_page='user_instrucoes.userinstrucoes', dados=dados_do_banco) 
    else:
        return redirect(url_for('login.login'))

@user_iso_routes.route('/user_iso')
def useriso():
    if 'username' in session and 'role' in session and session['role'] == "user":
        categoria = 'ISO'  # Defina a categoria desejada
        dados_do_banco = obter_dados_do_banco_por_categoria(categoria)
        return render_template('user_iso.html', active_page='user_iso.useriso', dados=dados_do_banco) 
    else:
        return redirect(url_for('login.login'))

@user_documentos_gerais_routes.route('/user_documentos_gerais')
def userdocumentosgerais():
    if 'username' in session and 'role' in session and session['role'] == "user":
        categoria = 'Documentos Gerais'  # Defina a categoria desejada
        dados_do_banco = obter_dados_do_banco_por_categoria(categoria)
        return render_template('user_documentos_gerais.html', active_page='user_documentos_gerais.userdocumentosgerais', dados=dados_do_banco) 
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

@admin_pdf_edit_routes.route('/edit', methods=['POST'])
def edit():
    if 'username' in session and 'role' in session and session['role'] == "admin":
        id_pdf = request.form.get('edit_id_pdf')  
        nome = request.form.get('edit_nome')       
        categoria = request.form.get('edit_categoria') 
        data = request.form.get('edit_data')   
        arquivo = request.files['arquivo']
        pdf_edit(id_pdf, nome, categoria, data, arquivo)
        
        return redirect(url_for('pdf.pdf'))
    else:
        return redirect(url_for('login.login'))
    
@admin_pdf_delete_routes.route('/delete', methods=['POST'])
def delete():
    if 'username' in session and 'role' in session and session['role'] == "admin":
        id_pdf = request.form.get('id_pdf')  
        pdf_delete(id_pdf)
        
        return redirect(url_for('pdf.pdf'))
    else:
        return redirect(url_for('login.login'))


@admin_pdf_generate_routes.route('/generate', methods=['POST'])
def generate():
    if 'username' in session and 'role' in session and session['role'] == "admin":
        # Obter dados do formulário
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')
        versao = request.form.get('versao')
        data = request.form.get('data')
        arquivo = request.files['arquivo'] if 'arquivo' in request.files else None
        processar_formulario(nome, categoria, versao, data, arquivo)
        
        return redirect(url_for('pdf.pdf'))
    else:
        return redirect(url_for('login.login'))
    

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
        processar_formulario_user(nome, cargo, role, senha)
        
        return redirect(url_for('usuarios.usuarios'))
    else:
        return redirect(url_for('login.login'))
    
@admin_user_edit_routes.route('/edituser', methods=['POST'])
def edituser():
    if 'username' in session and 'role' in session and session['role'] == "admin":
        id_user = request.form.get('edit_id_user')  
        nome = request.form.get('edit_nome')
        cargo = request.form.get('edit_cargo')
        role = request.form.get('edit_role')
        senha = request.form.get('edit_senha')
        print(id_user, nome, cargo, role, senha)
        user_edit(id_user, nome, cargo, role, senha)
        
        return redirect(url_for('usuarios.usuarios'))
    else:
        return redirect(url_for('login.login'))
    
@admin_user_delete_routes.route('/deleteuser', methods=['POST'])
def deleteuser():
    if 'username' in session and 'role' in session and session['role'] == "admin":
        id_user = request.form.get('id_user')  
        user_delete(id_user)
        
        return redirect(url_for('usuarios.usuarios'))
    else:
        return redirect(url_for('login.login'))

@logout_routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.login'))