from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label='Имя пользователя', max_length=20)
    email = serializers.EmailField(label='Email', max_length=50)
    first_name = serializers.CharField(label='Имя', max_length=15)
    last_name = serializers.CharField(label='Фамилия', max_length=15)
    password = serializers.CharField(label='Пароль', style={'input_type': 'password'}, write_only=True, min_length=6)
    confirm_password = serializers.CharField(
        label='Подтвердить пароль', style={'input_type': 'password'}, write_only=True, min_length=6
    )

    class Meta:
        model = Profile
        fields = ('username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'gender', 'avatar')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Пароли не совпадают!')
        return data

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(f'Пользователь с ником {value} уже существует')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(f'Пользователь с email {value} уже существует')
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        profile = Profile(
            user=user,
            gender=validated_data['gender'],
            avatar=validated_data['avatar'],
        )
        profile.save()
        return user
