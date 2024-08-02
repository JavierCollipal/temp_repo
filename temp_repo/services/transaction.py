import logging
from datetime import datetime
from uuid import UUID
from mongoengine.errors import ValidationError, BulkWriteError
from ..models.transaction import Transaction
from ..models.keyword import Keyword
import traceback

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cached keyword mappings
keyword_cache = {}

def list_transactions():
    return Transaction.objects.all()

def create_transaction(data):
    transaction = Transaction(**data)
    transaction.save()
    return transaction

def get_enriched_data(transaction, merchant_id=None, category_id=None):
    return {
        'external_id': str(transaction.external_id),
        'description': transaction.description,
        'amount': transaction.amount,
        'date': transaction.date,
        'category': category_id,  # Make sure category_id is correctly fetched
        'commerce': merchant_id   # Make sure merchant_id is correctly fetched
    }

def log_description(transaction):
    description = transaction.description.lower()
    logger.info(f"Description for transaction ID: {transaction.external_id}: {description}")
    return description

def load_keyword_cache():
    global keyword_cache
    keywords = Keyword.objects.all()
    for keyword in keywords:
        keyword_cache[keyword.keyword.lower()] = {
            'merchant_id': keyword.merchant_id.id,  # Use ID to avoid object reference issues
            'category_id': keyword.merchant_id.category.id if keyword.merchant_id and keyword.merchant_id.category else None
        }
    logger.info(f"Loaded {len(keyword_cache)} keywords into cache.")

def find_keyword(description):
    for keyword, data in keyword_cache.items():
        if keyword in description:
            return data
    return None

def handle_enrichment_error(transaction_id, error):
    logger.error(f"Error during enrichment for transaction ID: {transaction_id}: {str(error)}")
    logger.error("Traceback:", exc_info=True)  # This logs the stack trace

def calculate_metrics(enriched_transactions, total_transactions_received, total_keyword_matches):
    successful_categorizations = sum(1 for tx in enriched_transactions if tx.get('category') is not None)
    successful_identifications = sum(1 for tx in enriched_transactions if tx.get('commerce') is not None)
    match_keyword_rate = (total_keyword_matches / total_transactions_received) * 100 if total_transactions_received > 0 else 0

    categorization_rate = (successful_categorizations / total_transactions_received) * 100 if total_transactions_received > 0 else 0
    merchant_identification_rate = (successful_identifications / total_transactions_received) * 100 if total_transactions_received > 0 else 0

    logger.info(f"Total Transactions Received: {total_transactions_received}")
    logger.info(f"Categorization Rate: {categorization_rate:.2f}%")
    logger.info(f"Merchant Identification Rate: {merchant_identification_rate:.2f}%")
    logger.info(f"Match Keyword Rate: {match_keyword_rate:.2f}%")

    return {
        'total_transactions_received': total_transactions_received,
        'categorization_rate': categorization_rate,
        'merchant_identification_rate': merchant_identification_rate,
        'match_keyword_rate': match_keyword_rate
    }

def enrich_transaction(transaction):
    logger.info(f"Starting enrichment for transaction ID: {transaction.external_id}")
    description = log_description(transaction)

    keyword_data = find_keyword(description)
    commerce = keyword_data['merchant_id'] if keyword_data else None
    category = keyword_data['category_id'] if keyword_data else determine_category_from_description(description)

    transaction.category = category
    transaction.commerce = commerce
    transaction.updated_at = datetime.utcnow()

    return transaction

def determine_category_from_description(description):
    if "tienda de abarrotes" in description or "supermercado" in description:
        return "your-predefined-uuid-for-supermarket-category"  # Replace with actual UUID
    return None

def enrich_transactions(transactions):
    load_keyword_cache()
    total_transactions_received = len(transactions)
    total_keyword_matches = 0
    enriched_transactions_data = []
    enriched_transaction_objects = []

    for transaction in transactions:
        try:
            description = log_description(transaction)
            keyword_data = find_keyword(description)

            if keyword_data:
                total_keyword_matches += 1
            
            enriched_transaction = enrich_transaction(transaction)
            enriched_transactions_data.append(get_enriched_data(
                enriched_transaction,
                merchant_id=enriched_transaction.commerce,
                category_id=enriched_transaction.category
            ))

            enriched_transaction_objects.append(enriched_transaction)
            
        except Exception as e:
            handle_enrichment_error(transaction.external_id, e)

    # Bulk insert enriched transaction objects
    try:
        if enriched_transaction_objects:
            Transaction.objects.insert(enriched_transaction_objects, load_bulk=False)
            logger.info(f"Bulk insert completed for {len(enriched_transaction_objects)} transactions.")
    except Exception as e:
        logger.error(f"Error during bulk insert: {e}")

    metrics = calculate_metrics(enriched_transactions_data, total_transactions_received, total_keyword_matches)
    return metrics