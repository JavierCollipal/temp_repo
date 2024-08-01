from rest_framework import generics
from ..serializers.transaction import TransactionSerializer
from ..services.transaction import list_transactions, create_transaction

class TransactionListCreate(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return list_transactions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_transaction(serializer.validated_data)
        return super().create(request, *args, **kwargs)
