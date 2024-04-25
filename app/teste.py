import pusher
import datetime

pusher_client = pusher.Pusher(
  app_id='1793305',
  key='f92025bb780d9ff681ff',
  secret='77017a5aa538e7d496b8',
  cluster='sa1',
  ssl=True
)

data = {
        'nome': 'Documento de Teste',
        'versao': '1.0',
        'timestamp': datetime.now().isoformat(),
        'anotacoes': 'Este é um documento de teste'
    }

pusher_client.trigger('my-channel', 'new-document', data)