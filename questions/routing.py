from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/public', consumers.PublicQuestionsConsumer.as_asgi()),
    path('ws/moderator', consumers.ModeratorQuestionsConsumer.as_asgi()),
    path('ws/display', consumers.DisplayQuestionsConsumer.as_asgi()),
]