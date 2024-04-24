import pusher

pusher_client = pusher.Pusher(
  app_id='1793305',
  key='f92025bb780d9ff681ff',
  secret='77017a5aa538e7d496b8',
  cluster='sa1',
  ssl=True
)

pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})