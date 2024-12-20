from django.urls import path
from .views import BlogDetailView,BlogCreateView,BlogUpdateView,BlogDeleteView


urlpatterns = [
    path('detail/<int:id>/', BlogDetailView.as_view(), name='blog/list'),
    path('create/', BlogCreateView.as_view(), name='blog/create'),
    path('update/<int:id>/', BlogUpdateView.as_view(), name='blog/update'),
    path('delete/<int:id>/', BlogDeleteView.as_view(), name='blog/delete'),
]