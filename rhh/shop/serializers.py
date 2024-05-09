from django.contrib.auth import models
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from shop.models import DjangoUser, MessageUs


class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoUser
        fields = ('id', 'email', 'password', 'first_name',
                  'last_name', 'username', 'is_active', 'age', 'address', 'phone')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'write_only': True, 'validators': []}
        }


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageUs
        fields = '__all__'
