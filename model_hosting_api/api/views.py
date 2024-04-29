from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RequestLog
from .serializers import RequestLogSerializer
from .load_model import load_model
from transformers import pipeline
import torch
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework.views import APIView
from .utils import run_prompt

# Create your views here.

generator = load_model()


class ChatWithAI(APIView):
    async def get(self, request):
        prompt = request.query_params.get('prompt', 'Hello world')
        response = await run_prompt(prompt)
        return JsonResponse({'response': response})


# Django View for generating text
class GenerateTextView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generator = load_model()  # Load the model when the view is initialized

    def post(self, request):
        request_text = request.data.get('request_text', None)
        if request_text is None:
            return Response({'error': 'String is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not self.generator:
            return Response({'error': 'Model is not loaded'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            response = self.generator([{
                "role": "user", "content": request_text
            }], max_new_tokens=100, return_full_text=False, temperature=0.0, do_sample=False)[0]['generated_text']

            log = RequestLog.objects.create(
                request_text=request_text, response_text=response)
            serializer = RequestLogSerializer(log)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Failed to generate text: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
