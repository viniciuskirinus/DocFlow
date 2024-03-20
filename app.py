from app import create_app

# Cria a instância do aplicativo Flask
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
