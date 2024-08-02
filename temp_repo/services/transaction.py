from ..models.transaction import Transaction
from ..models.commerce import Commerce
from ..models.category import Category
from ..models.keyword import Keyword
from mongoengine.errors import ValidationError

def list_transactions():
    return Transaction.objects.all()

def create_transaction(data):
    transaction = Transaction(**data)
    transaction.save()
    return transaction

def create_transactions(data, max_batch_size=500):
    actual_batch_size = min(max_batch_size, len(data))
    transactions = [Transaction(**item) for item in data]
    for i in range(0, len(transactions), actual_batch_size):
        Transaction.objects.insert(transactions[i:i+actual_batch_size])

def enrich_transaction(transaction):
    """
    Enrich a single transaction with commerce and category details.
    """
    description = transaction.description.lower()
    keywords = Keyword.objects.all()
    matched_keyword = next((kw for kw in keywords if kw.keyword.lower() in description), None)

    if matched_keyword:
        try:
            commerce = Commerce.objects.get(id=matched_keyword.merchant_id)
            enriched_data = {
                'id': str(transaction.id),
                'description': transaction.description,
                'amount': transaction.amount,
                'date': transaction.date,
                'category_id': str(commerce.category.id),
                'commerce_id': str(commerce.id),
                'merchant_name': commerce.merchant_name,
                'merchant_logo': commerce.merchant_logo
            }
        except Commerce.DoesNotExist:
            enriched_data = {
                'id': str(transaction.id),
                'description': transaction.description,
                'amount': transaction.amount,
                'date': transaction.date,
                'category_id': None,
                'commerce_id': None,
                'merchant_name': None,
                'merchant_logo': None
            }
    else:
        enriched_data = {
            'id': str(transaction.id),
            'description': transaction.description,
            'amount': transaction.amount,
            'date': transaction.date,
            'category_id': None,
            'commerce_id': None,
            'merchant_name': None,
            'merchant_logo': None
        }
    
    return enriched_data

def enrich_transactions(transactions):
    """
    Enrich multiple transactions.
    """
    enriched_transactions = []
    for transaction in transactions:
        enriched_data = enrich_transaction(transaction)
        enriched_transactions.append(enriched_data)

    return enriched_transactions