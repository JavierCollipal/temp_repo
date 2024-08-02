from rest_framework import generics, status
from rest_framework.response import Response
from ..serializers.transaction import TransactionSerializer
from ..serializers.enrichment import EnrichedTransactionSerializer
from rest_framework.response import Response
from ..models.transaction import Transaction
from ..services.transaction import list_transactions, create_transaction, create_transaction, enrich_transactions
class TransactionListCreate(generics.GenericAPIView):
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

class EnrichmentOperationView(generics.GenericAPIView):
    """
    API endpoint for enriching transactions with additional information like commerce and category.
    """
    serializer_class = TransactionSerializer
    
    def post(self, request, *args, **kwargs):
        transactions_data = request.data.get('transactions', [])
        
        # Validate and collect transactions
        transactions = self.validate_and_collect_transactions(transactions_data)
        
        # Perform enrichment
        metrics = enrich_transactions(transactions)

        return Response(metrics, status=status.HTTP_200_OK)

    def validate_and_collect_transactions(self, transactions_data):
        """
        Validates the transactions data and collects valid transactions.
        
        Args:
            transactions_data (list): List of transaction data dictionaries.
        
        Returns:
            list: List of valid transaction objects.
        """
        transactions = []
        for data in transactions_data:
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                transaction = serializer.save()
                transactions.append(transaction)
            else:
                print("[ERROR] Invalid transaction data:", serializer.errors)
        
        return transactions