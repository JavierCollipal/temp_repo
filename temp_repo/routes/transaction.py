from django.urls import path
from ..views.transaction import TransactionListCreate

urlpatterns = [
    path('transactions/', TransactionListCreate.as_view(), name='transaction-list-create'),
]
