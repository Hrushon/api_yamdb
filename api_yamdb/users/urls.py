from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserViewSet, MeUserAPIView, SignUpViewSet, TokenViewSet

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('auth/signup', SignUpViewSet, basename='sign-up')
router_v1.register('auth/token', TokenViewSet, basename='token')

urlpatterns = [
    #path('/users/me/', UserMeViewSet.as_view()),
    #path('/auth/signup/', ),
    #path('/auth/token/', ),


    path('v1/users/me/', MeUserAPIView.as_view()),
    path('v1/', include(router_v1.urls)),
    
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
