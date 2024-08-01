from rest_framework import generics, status
from rest_framework.response import Response
from ..serializers.transaction import TransactionSerializer
from ..services.transaction import list_transactions, create_transaction, create_transactions

class TransactionListCreate(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return list_transactions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_transaction(serializer.validated_data)
        return super().create(request, *args, **kwargs)

class TransactionCreateMany(generics.GenericAPIView):
    serializer_class = TransactionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        create_transactions(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
