from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow
from oauth2client.file import Storage
import webbrowser
import os
import json

# Configurar as informações do cliente OAuth
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET ")
SCOPE = 'https://www.googleapis.com/auth/drive'

# Configurar o fluxo de autorização
flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                           client_secret=CLIENT_SECRET,
                           scope=SCOPE,
                           redirect_uri='http://localhost:8080/oauth2callback')

# Obter o código de autorização automaticamente e abrir a página de autorização
auth_uri = flow.step1_get_authorize_url()
webbrowser.open(auth_uri)

# Trocar o código de autorização por tokens de acesso e atualização
credentials = run_flow(flow, Storage('credentials.json'))

# Salvar as credenciais em um arquivo de texto
with open('credentials.txt', 'w') as f:
    f.write(json.dumps(credentials.to_json()))
