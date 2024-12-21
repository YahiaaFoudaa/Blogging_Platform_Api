from django.urls import path
from .views import UserListView,UserLoginView,UserRegisterView,UserUpdateView, UserLogoutView

urlpatterns = [
    path('user/list/', UserListView.as_view(), name='user/list'),
    path('user/login/', UserLoginView.as_view(), name='user/login'),
    path('user/register/', UserRegisterView.as_view(), name='user/register'),
    path('user/update/<int:user_id>/', UserUpdateView.as_view(), name='user/update'),
    path('user/logout/', UserLogoutView.as_view(), name='user/logout'),
]