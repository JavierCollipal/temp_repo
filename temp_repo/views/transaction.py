from rest_framework import generics, status
from rest_framework.response import Response
from ..serializers.transaction import TransactionSerializer
from ..serializers.enrichment import EnrichedTransactionSerializer
from rest_framework.response import Response
from ..services.transaction import  enrich_transactions, get_enriched_transactions
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
    
    def get(self, request, *args, **kwargs):
        print("[GET] Retrieving list of enriched transactions.")
        enriched_transactions = get_enriched_transactions()
        serializer = TransactionSerializer(enriched_transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)