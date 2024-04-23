from app import create_app
from flask_socketio import SocketIO

# Cria a instância do aplicativo Flask
app = create_app()
socketio = SocketIO(app)  # Inicializa o SocketIO com o aplicativo Flask

if __name__ == '__main__':
    socketio.run(app)  # Executa o aplicativo Flask com o SocketIO