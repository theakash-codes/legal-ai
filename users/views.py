from ml.predict import predict_text
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email', '')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'username and password required'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'username exists'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, email=email, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'username': user.username})

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email', '').strip()
    password = request.data.get('password', '').strip()

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Try to find user by email first, then by username
    user = None
    try:
        user_obj = User.objects.get(email=email)
        user = authenticate(username=user_obj.username, password=password)
    except User.DoesNotExist:
        # Try treating email as username
        user = authenticate(username=email, password=password)

    if user is None:
        # Auto-create account if it doesn't exist
        username = email.split('@')[0] if '@' in email else email
        # Ensure unique username
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        user = User.objects.create_user(username=username, email=email if '@' in email else '', password=password)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'username': user.username})

@api_view(['POST'])
def logout_view(request):
    token_key = request.META.get('HTTP_AUTHORIZATION')
    if token_key:
        try:
            token = Token.objects.get(key=token_key.split()[1])
            token.delete()
        except:
            pass
    return Response({'detail': 'logged out'})

def home(request):  # <- No decorator here!
    return render(request, "index.html")
