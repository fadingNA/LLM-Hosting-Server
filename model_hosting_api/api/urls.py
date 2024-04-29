# api/urls.py

from django.urls import path
from .views import GenerateTextView, ChatWithAI

urlpatterns = [
    path('chat/', ChatWithAI.as_view(), name='chat-with-ai'),
    path('generate-text/', GenerateTextView.as_view(), name='generate-text'),
]
