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
