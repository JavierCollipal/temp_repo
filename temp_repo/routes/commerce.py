from django.urls import path
from ..views.commerce import CommerceListCreateView, CommerceDetailView

urlpatterns = [
    path('commerces/', CommerceListCreateView.as_view(), name='commerce-list-create'),
    path('commerces/<uuid:commerce_id>/', CommerceDetailView.as_view(), name='commerce-detail'),
]
