from django.shortcuts import render

# Create your views here.
# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def home(request):
    return Response({
        "message": "Hello from Django"
    })