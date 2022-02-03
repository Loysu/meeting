from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Профиль пользователя (главная модель)"""
    MALE = 'male'
    FEMALE = 'female'

    GENDER_CHOICES = [
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина'),
    ]

    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    gender = models.CharField('Пол', max_length=10, choices=GENDER_CHOICES)
    avatar = models.ImageField('Аватарка', upload_to='avatars/')

    def __str__(self):
        return self.user.username
