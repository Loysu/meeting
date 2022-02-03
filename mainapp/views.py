from django.contrib.auth import login, authenticate
from django.shortcuts import redirect

from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.reverse import reverse

from .serializers import SignupSerializer


class SignupView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'mainapp/sign_up.html'

    def get(self, request):
        serializer = SignupSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = authenticate(
                username=serializer.validated_data['username'], password=serializer.validated_data['password']
            )
            login(request, user)
            return redirect(reverse('mainapp:base'))
        return Response({'serializer': serializer})
