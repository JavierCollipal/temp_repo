from django.urls import path
from ..views.keyword import KeywordListCreateView, KeywordDetailView

urlpatterns = [
    path('keywords/', KeywordListCreateView.as_view(), name='keyword-list-create'),
    path('keywords/<uuid:keyword_id>/', KeywordDetailView.as_view(), name='keyword-detail'),
]