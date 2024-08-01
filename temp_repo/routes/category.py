from django.urls import path
from ..views.category import CategoryListCreateView, CategoryDetailView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<uuid:category_id>/', CategoryDetailView.as_view(), name='category-detail'),
]