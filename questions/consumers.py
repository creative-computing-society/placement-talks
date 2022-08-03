from channels.consumer import AsyncConsumer, SyncConsumer, StopConsumer
from channels.db import database_sync_to_async
import json
from .models import Question

class PublicQuestionsConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("websocket connected...")
        await self.send({
            'type': 'websocket.accept'
        })
    
    async def websocket_receive(self, event):
        # print(event)
        data = json.loads(event['text'])
        # print(data)
        question = Question(text=data['text'])
        question = await database_sync_to_async(question.save)()
        print(question)
        await self.send({
            'type': 'websocket.send',
            'text': json.dumps({'id': question.id, 'text': question.text})
        })
    
    async def websocket_disconnect(self, event):
        print(event, "public websocket disconnected...")
        raise StopConsumer()

class ModeratorQuestionsConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("moderator websocket connected...")
        await self.send({
            'type': 'websocket.accept',
        })
    
    async def websocket_receive(self, event):
        # print(event)
        data = json.loads(event['text'])
        print(data)
        await self.send({
            'type': 'websocket.send',
            'text': json.dumps({'message': 'hello from moderator consumer'})
        })
    
    async def websocket_disconnect(self, event):
        print(event, "moderator websocket disconnected...")
        raise StopConsumer()

class DisplayQuestionsConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print(event, "Output websocket connected...")
        self.send({
            'type': 'websocket.accept',
        })
    
    def websocket_receive(self, event):
        # print(event)
        data = json.loads(event['text'])
        print(data)
        self.send({
            'type': 'websocket.send',
            'text': json.dumps({'message': 'hello from display consumer'})
        })
    
    def websocket_disconnect(self, event):
        print(event, "output websocket disconnected...")
        raise StopConsumer()
