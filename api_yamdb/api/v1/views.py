from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from users.models import User
from .filters import TitleFilter
from .permissions import (IsAdminOnlyPermission, IsAdminOrReadOnlyPermission,
                          IsAuthorModeratorAdminOrReadOnlyPermission,
                          SelfEditUserOnlyPermission)
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, ReviewSerializer,
                          TitlesGettingSerializer, TitlesSerializer,
                          UserMeSerializer, UserSerializer,
                          UserSignUpSerializer, UserTokenSerializer)


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """База для реализации методов GET, POST, DEL."""
    pass


class CategoriesViewSet(ListCreateDestroyViewSet):
    """Реализует методы GET, POST, DEL для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnlyPermission,)


class GenresViewSet(ListCreateDestroyViewSet):
    """Реализует методы GET, POST, DEL для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnlyPermission,)


class TitlesViewSet(viewsets.ModelViewSet):
    """Работает над всеми операциями с произведениями."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    serializer_class = TitlesGettingSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesGettingSerializer
        return TitlesSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Работает над всеми операциями с комментариями к отзывам."""
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthorModeratorAdminOrReadOnlyPermission
    ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """Работает над всеми операциями с отзывами."""
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorModeratorAdminOrReadOnlyPermission
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title_id=self.kwargs.get('title_id')
        )


class UserViewSet(viewsets.ModelViewSet):
    """
    Работает над всеми операциями с пользователями от лица админа.
    Позволяет обычному пользователю редактировать свой профиль.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdminOnlyPermission,)

    @action(
        methods=['get', 'patch'], detail=False,
        url_path='me', permission_classes=(SelfEditUserOnlyPermission,)
    )
    def me_user(self, request):
        if request.method == 'GET':
            user = User.objects.get(username=request.user)
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        user = User.objects.get(username=request.user)
        serializer = UserMeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Осуществляет регистрацию пользователей.
    Отправляет confirmation_code на электронную почту пользователя
    как при регистрации, так и при повторном валидном обращении.
    А также в случае, если пользователя зарегистрировал администратор.
    """
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if (User.objects.filter(username=request.data.get('username'),
                                email=request.data.get('email'))):
            user = User.objects.get(username=request.data.get('username'))
            serializer = UserSignUpSerializer(user, data=request.data)
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


class TokenViewSet(viewsets.ViewSet):
    """
    Осуществляет выдачу зарегистрированному пользователю.
    Обновляет истекший токен.
    """
    permission_classes = (permissions.AllowAny,)

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
                token = {'token': str(refresh.access_token)}
                return Response(
                    token, status=status.HTTP_200_OK
                )
            return Response(
                context, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
