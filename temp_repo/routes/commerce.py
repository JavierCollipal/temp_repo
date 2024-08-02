from django.urls import path, re_path
from ..views.commerce import CommerceListCreateView, CommerceDetailView

urlpatterns = [
    path('commerces/', CommerceListCreateView.as_view(), name='commerce-list-create'),
    re_path(r'^commerces/(?P<commerce_id>[0-9a-f]{24})/$', CommerceDetailView.as_view(), name='commerce-detail'),
]
