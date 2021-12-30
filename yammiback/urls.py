from django.urls import path
from .views import MyTokenObtainPairView, RegisterView, getRoutes, UserLoginView, AllUsersListView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', getRoutes),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('users/', AllUsersListView.as_view(), name='users')
]
