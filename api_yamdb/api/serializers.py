from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from reviews.models import User


class GetTokenSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User


class GetConfirmationCode(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        model = User
