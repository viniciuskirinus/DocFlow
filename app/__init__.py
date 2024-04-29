from flask import Flask


def create_app():
    app = Flask(__name__)

    # Configurações do aplicativo podem ser carregadas de config.py
    app.config.from_pyfile('config.py')

    # Registra as blueprints (rotas) do aplicativo
    from app.routes import (admin_routes, 
                            home_routes, 
                            login_routes, 
                            logout_routes, 
                            admin_pdf_routes, 
                            admin_user_routes, 
                            admin_pdf_generate_routes, 
                            admin_pdf_edit_routes, 
                            admin_pdf_delete_routes, 
                            user_procedimentos_routes, 
                            user_manuais_routes, 
                            user_instrucoes_routes, 
                            user_iso_routes, 
                            user_documentos_gerais_routes, 
                            process_chat_routes, 
                            admin_user_generate_routes, 
                            admin_user_delete_routes, 
                            admin_user_edit_routes, 
                            user_show_pdf_routes,
                            admin_old_files_routes,
                            admin_old_files_send_routes, 
                            user_projetos_routes,
                            user_documentos_clientes_routes,
                            user_politicas_gerais_routes,
                            user_edit_data_routes,
                            marcar_todas_como_lidas_routes)
    
    # Registrando as blueprints
    app.register_blueprint(login_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(admin_old_files_routes)
    app.register_blueprint(admin_old_files_send_routes)
    app.register_blueprint(home_routes)
    app.register_blueprint(user_procedimentos_routes)
    app.register_blueprint(user_manuais_routes)
    app.register_blueprint(user_instrucoes_routes)
    app.register_blueprint(user_iso_routes)
    app.register_blueprint(user_documentos_gerais_routes)
    app.register_blueprint(user_projetos_routes)
    app.register_blueprint(user_documentos_clientes_routes)
    app.register_blueprint(user_politicas_gerais_routes)
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
    app.register_blueprint(user_edit_data_routes)
    app.register_blueprint(marcar_todas_como_lidas_routes)
    app.register_blueprint(logout_routes)

    return app
