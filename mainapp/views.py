from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.reverse import reverse

from .filters import ProfileFilter
from .serializers import ProfileSerializer
from .models import Profile, Relationship


class Signup(APIView):
    """Регистрация"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'mainapp/sign_up.html'

    def get(self, request):
        serializer = ProfileSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = authenticate(
                username=serializer.validated_data['user']['username'],
                password=serializer.validated_data['user']['password']
            )
            login(request, user)
            return redirect(reverse('mainapp:base'))
        return Response({'serializer': serializer})


class ProfileDetail(APIView):
    """Главная страница пользователя"""

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Profile, pk=pk)

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request, pk):
        profile1 = request.user.profile
        profile2 = self.get_object(pk)
        if not Relationship.objects.filter(Q(main_profile=profile1) & Q(profile=profile2)).exists():
            Relationship.objects.create(main_profile=profile1, profile=profile2)
            if Relationship.objects.filter(Q(main_profile=profile2) & Q(profile=profile1)).exists():
                subject = '♡У вас появился потенциальный партнер!♡'
                self.send_message(profile1, profile2, subject)
                self.send_message(profile2, profile1, subject)
                return Response(f'Почта участница - {profile2.user.email}')
            return Response('Участник успешно добавлен в ваш список!')
        return Response(f'Участник уже в вашем списке!')

    @staticmethod
    def send_message(profile1, profile2, subject):
        return profile2.user.email_user(
            subject,
            message=f'{profile1.user.first_name} заинтересован{"а" if profile1.gender == "female" else ""} в вас! '
                    f'Почта участника - {profile1.user.email}'
        )


class ProfileList(generics.ListAPIView):
    """Список профилей с возможной фильтрацией по полу, имени или фамилии"""
    serializer_class = ProfileSerializer
    filterset_class = ProfileFilter

    def get_queryset(self):
        return Profile.objects.exclude(user=self.request.user)
