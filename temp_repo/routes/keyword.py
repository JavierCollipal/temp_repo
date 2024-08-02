from django.urls import path, re_path
from ..views.keyword import KeywordListCreateView, KeywordDetailView

urlpatterns = [
    path('keywords/', KeywordListCreateView.as_view(), name='keyword-list-create'),
    re_path(r'^keywords/(?P<keyword_id>[0-9a-f]{24})/$', KeywordDetailView.as_view(), name='keyword-detail'),
]