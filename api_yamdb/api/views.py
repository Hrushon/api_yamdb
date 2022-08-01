from rest_framework import viewsets
from reviews.models import Categories, Titles, Genres
from .serializers import (CategoriesSerializer, GenresSerializer,
                          TitlesGettingSerializer, TitlesSerializer)

from .permissions import AdminOrReadOnly


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AdminOrReadOnly,)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (AdminOrReadOnly,)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesGettingSerializer
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list':
            return TitlesGettingSerializer
        elif self.action == 'retrieve':
            return TitlesGettingSerializer
        else:
            return TitlesSerializer
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review, Titles
from users.permissions import IsAuthorModeratorAdminOrReadOnlyPermission


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorModeratorAdminOrReadOnlyPermission
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorModeratorAdminOrReadOnlyPermission
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title_id=self.kwargs.get('title_id')
        )
