import re

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from PIL import Image


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
    avatar = models.ImageField('Аватар', upload_to='avatars/')

    def __str__(self):
        return self.user.username

    def add_watermark(self, wm=f'{settings.MEDIA_ROOT}/watermark.png'):
        # Добавление водяного знака на аватар профиля
        img = self.avatar
        image = Image.open(img)
        watermark = Image.open(wm)
        new_width = 200
        ratio = new_width / watermark.width
        new_height = int(watermark.height * ratio)
        watermark.thumbnail((new_width, new_height))  # уменьшение водяного знака в размере
        image.paste(watermark, (0, 0))
        avatar_name = re.sub(r'^\S+/|\.\S+$', '', self.avatar.name)
        name = self.avatar.name
        new_avatar_name = name.replace(avatar_name, f'{avatar_name}_watermarked')
        image.save(f'{settings.MEDIA_ROOT}\\avatars\\{new_avatar_name}')
        return f'\\avatars\\{new_avatar_name}'

    def save(self, *args, **kwargs):
        if '_watermarked' not in self.avatar.name:
            self.avatar = self.add_watermark()
        super().save(*args, **kwargs)


class Relationship(models.Model):
    """Модель отношений между пользователями"""
    main_profile = models.ForeignKey(
        Profile, verbose_name='Основной профиль профиль', related_name='main_profile', on_delete=models.CASCADE,
        help_text='Профиль пользователя, которому понравился другой пользователь'
    )
    profile = models.ForeignKey(
        Profile, verbose_name='Второй профиль', on_delete=models.CASCADE,
        help_text='Профиль понравившегося пользователя'
    )

    def __str__(self):
        return self.main_profile.user.username + ' | ' + self.profile.user.username
