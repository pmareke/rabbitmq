from src.consumer import Consumer

consumer = Consumer(lambda message: print(message))
consumer.start()
