from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from reviews.models import User
from .serializers import GetTokenSerializer, GetConfirmationCode


@api_view(['POST'])
@permission_classes([AllowAny],)
def get_confirmation_code(request):
    if request.method == 'POST':
        serializer = GetConfirmationCode(data=request.data)
        if serializer.is_valid():
            send_mail(
                'Title: your confirmation_code',
                'bgfhbgrg7896gwuvfwbfubv',
                'artem@gmail.com',
                ['garry@gmail.com'],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny],)
def get_token(request):
    if request.method == 'POST':
        serializer = GetTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            token = default_token_generator.make_token(user)
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
