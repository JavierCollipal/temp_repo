from django.urls import path, re_path
from ..views.category import CategoryListCreateView, CategoryDetailView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    re_path(r'^categories/(?P<category_id>[0-9a-f]{24})/$', CategoryDetailView.as_view(), name='category-detail'),
]