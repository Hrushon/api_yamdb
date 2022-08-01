from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

#from rest_framework.permissions import (IsAuthenticated,
#                                        IsAuthenticatedOrReadOnly)
from reviews.models import Categories, Genres, Review, Titles
from users.permissions import (
    IsAdminOrReadOnlyPermission,
    IsAuthorModeratorAdminOrReadOnlyPermission,
)

from .serializers import (
    CategoriesSerializer,
    CommentSerializer,
    GenresSerializer,
    ReviewSerializer,
    TitlesGettingSerializer,
    TitlesSerializer,
)


class CategoriesViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnlyPermission,)


class GenresViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnlyPermission,)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesGettingSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesGettingSerializer
        return TitlesSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthorModeratorAdminOrReadOnlyPermission
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
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
