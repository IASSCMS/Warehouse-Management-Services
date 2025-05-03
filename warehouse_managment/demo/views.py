from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(['GET'])
def check_endpoint(request):
    return Response({"message": "This is a simple check endpoint using DRF."})