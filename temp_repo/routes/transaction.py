from django.urls import path
from ..views.transaction import EnrichmentOperationView  

urlpatterns = [
    path('transactions/enrich/', EnrichmentOperationView.as_view(), name='enrichment-operation'),
]