from django.urls import path
from ..views.transaction import TransactionListCreate, TransactionCreateMany,  EnrichmentOperationView  

urlpatterns = [
    path('transactions/', TransactionListCreate.as_view(), name='transaction-list-create'),
    path('transactions/create_many/', TransactionCreateMany.as_view(), name='transaction-create-many'),
    path('transactions/enrich/', EnrichmentOperationView.as_view(), name='enrichment-operation'),
]