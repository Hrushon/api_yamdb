from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdminOnlyPermission, SelfEditUserOnlyPermission
from .serializers import UserSerializer, UserTokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminOnlyPermission,)


class MeUserAPIView(APIView):
    permission_classes = (SelfEditUserOnlyPermission,)

    def get(self, request):
        user = User.objects.get(id=1)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = User.objects.get(id=1)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpViewSet(viewsets.ViewSet):

    def create(self, request):
        context = 'Запрещено использовать me в качестве username'
        if request.data.get('username') != 'me':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                username = request.data.get('username')
                user = User.objects.get(username=username)
                code = user.confirmation_code
                send_mail(
                    f'Wellcome in YaMDb, {user.username}!',
                    (f'Скопируйте этот confirmation_code: {code} '
                     f'для получения и последующего обновления токена '
                     f'по адресу api/v1/auth/token/'),
                    'yamdb@yandex.ru',
                    [request.data.get('email')],
                    fail_silently=False,
                )
                return Response(
                    serializer.data, status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            context, status=status.HTTP_400_BAD_REQUEST
        )


class TokenViewSet(viewsets.ViewSet):

    def create(self, request):
        context = 'Проверьте confirmation_code'
        serializer = UserTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, username=request.data.get('username')
            )
            if str(user.confirmation_code) == request.data.get(
                'confirmation_code'
            ):
                refresh = RefreshToken.for_user(user)
                context = {'token': str(refresh.access_token)}
                return Response(
                    context, status=status.HTTP_200_OK
                )
            return Response(
                context, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
