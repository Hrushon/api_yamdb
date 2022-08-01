from django.urls import include, path
from rest_framework import routers
from api.views import (ReviewViewSet, CommentViewSet)

app_name = 'api'

router = routers.DefaultRouter()

router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include('users.urls')),
    path('v1/', include(router.urls)),
]
