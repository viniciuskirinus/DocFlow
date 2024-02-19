from flask import Flask


def create_app():
    app = Flask(__name__)

    # Configurações do aplicativo podem ser carregadas de config.py
    app.config.from_pyfile('config.py')
    


    # Registra as blueprints (rotas) do aplicativo
    from app.routes import admin_routes, home_routes, login_routes, logout_routes, admin_pdf_routes, admin_user_routes, admin_pdf_generate_routes, admin_pdf_edit_routes, admin_pdf_delete_routes, file_routes, user_procedimentos_routes, process_chat_routes, admin_user_generate_routes, admin_user_delete_routes, admin_user_edit_routes, user_show_pdf_routes
    
    
    
    
    app.register_blueprint(login_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(home_routes)
    app.register_blueprint(user_procedimentos_routes)
    app.register_blueprint(admin_pdf_routes)
    app.register_blueprint(user_show_pdf_routes)
    app.register_blueprint(admin_user_routes)
    app.register_blueprint(admin_user_generate_routes)
    app.register_blueprint(admin_pdf_generate_routes)
    app.register_blueprint(admin_pdf_edit_routes)
    app.register_blueprint(admin_pdf_delete_routes)
    app.register_blueprint(admin_user_edit_routes)
    app.register_blueprint(admin_user_delete_routes)
    app.register_blueprint(process_chat_routes)

    app.register_blueprint(file_routes)
    app.register_blueprint(logout_routes)

    return app
