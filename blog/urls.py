from django.urls import path
from .views import BlogDetailView,BlogCreateView,BlogUpdateView,BlogDeleteView, TagCreateView, CategoryCreateView, SearchView


urlpatterns = [
    path('detail/<int:id>/', BlogDetailView.as_view(), name='blog/list'),
    path('create/', BlogCreateView.as_view(), name='blog/create'),
    path('update/<int:id>/', BlogUpdateView.as_view(), name='blog/update'),
    path('delete/<int:id>/', BlogDeleteView.as_view(), name='blog/delete'),
    path('tag/create/', TagCreateView.as_view(), name='tag/create'),
    path('category/create/', CategoryCreateView.as_view(), name='category/create'),
    path('search/', SearchView.as_view(), name='search'),
]