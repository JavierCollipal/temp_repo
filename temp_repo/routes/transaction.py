from django.urls import path
from ..views.transaction import TransactionListCreate, TransactionCreateMany

urlpatterns = [
    path('transactions/', TransactionListCreate.as_view(), name='transaction-list-create'),
    path('transactions/create_many/', TransactionCreateMany.as_view(), name='transaction-create-many'),
]
