from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoriesViewSet,
    CommentViewSet,
    GenresViewSet,
    ReviewViewSet,
    SignUpViewSet,
    TitlesViewSet,
    TokenViewSet,
    UserViewSet,
)


app_name = 'api'

router = routers.DefaultRouter()

router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register('users', UserViewSet, basename='users')
router.register('auth/signup', SignUpViewSet, basename='sign-up')
router.register('auth/token', TokenViewSet, basename='token')

urlpatterns = [
    path('', include(router.urls)),
]
