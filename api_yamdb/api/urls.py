from django.urls import include, path
from rest_framework import routers

from .views import CategoriesViewSet, TitlesViewSet, GenresViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(r'genres', GenresViewSet, basename='genres')


app_name = 'api'


urlpatterns = [
    path('v1/', include('users.urls')),
    path('v1/', include(router.urls)),
]
