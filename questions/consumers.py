from channels.consumer import AsyncConsumer, StopConsumer
from channels.db import database_sync_to_async
import json

from channels.utils import asyncio
from .models import Question

class PublicQuestionsConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept'
        })
    
    async def websocket_receive(self, event):
        data = json.loads(event['text'])
        if 'text' not in data or 'questioner' not in data:
            await self.send({
                'type': 'websocket.close',
            })
            return
        question = Question(questioner=data['questioner'], text=data['text'], channelName=self.channel_name)
        question = await database_sync_to_async(question.save)()
        await self.send({
            'type': 'websocket.send',
            'text': json.dumps({
                'type': 'question',
                'id': question.id,
                'text': question.text
            })
        })
        await self.channel_layer.group_send(
            "moderator",
            {
                'type': 'moderator.send',
                'operation': 'question',
                'id': question.id,
                'questioner': question.questioner,
                'text': question.text,
            }
        )
        # await asyncio.sleep(20)
    
    async def websocket_disconnect(self, event):
        raise StopConsumer()
    
    async def status_send(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': json.dumps({
                'type': 'status',
                'id': event['id'],
                'isAccepted': event['isAccepted']
            })
        })

class ModeratorQuestionsConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.channel_layer.group_add("moderator", self.channel_name)
        await self.send({
            'type': 'websocket.accept',
        })
    
    async def websocket_receive(self, event):
        data = json.loads(event['text'])
        if 'id' not in data or 'isAccepted' not in data:
            await self.send({
                'type': 'websocket.close',
            })
            return
        question = await database_sync_to_async(Question.objects.filter(id=data['id']).first)()
        if question!=None and question.isAccepted!=data['isAccepted']:
            if question.isAccepted:
                question.isAccepted = False
                question = await database_sync_to_async(question.save)()
                await self.channel_layer.group_send(
                    "display",
                    {
                        'type': 'display.send',
                        'operation': 'remove',
                        'id': question.id,
                    }
                )
            else:
                question.isAccepted = data['isAccepted']
                question = await database_sync_to_async(question.save)()
                if data['isAccepted']:
                    await self.channel_layer.group_send(
                        "display",
                        {
                            'type': 'display.send',
                            'operation': 'question',
                            'id': question.id,
                            'questioner': question.questioner,
                            'text': question.text,
                        }
                    )
            await self.channel_layer.group_send(
                "moderator",
                {
                    'type': 'moderator.send',
                    'operation': 'status',
                    'id': question.id,
                    'isAccepted': data['isAccepted'],
                }
            )
            await self.channel_layer.send(
                question.channelName,
                {
                    'type': 'status.send',
                    'id': question.id,
                    'isAccepted': question.isAccepted,
                }
            )
    
    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard("moderator", self.channel_name)
        raise StopConsumer()
    
    async def moderator_send(self, event):
        if event['operation']=='question':
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({
                    'type': 'question',
                    'id': event['id'],
                    'questioner': event['questioner'],
                    'text': event['text'],
                })
            })
        else:
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({
                    'type': 'status',
                    'id': event['id'],
                    'isAccepted': event['isAccepted'],
                })
            })


class DisplayQuestionsConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.channel_layer.group_add("display", self.channel_name)
        await self.send({
            'type': 'websocket.accept',
        })
    
    async def websocket_receive(self, event):
        super()
    
    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard("display", self.channel_name)
        raise StopConsumer()
    
    async def display_send(self, event):
        if event['operation']=='question':
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({
                    'type': 'question',
                    'id': event['id'],
                    'questioner': event['questioner'],
                    'text': event['text'],
                })
            })
        else:
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({
                    'type': 'remove',
                    'id': event['id'],
                })
            })
