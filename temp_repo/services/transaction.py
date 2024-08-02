import logging
from datetime import datetime
from uuid import UUID
from mongoengine.errors import ValidationError, BulkWriteError
from ..models.transaction import Transaction
from ..models.keyword import Keyword
from ..models.category import Category  # Assuming you have a Category model for category search
import traceback

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        'category': category_id,
        'commerce': merchant_id
    }

def log_description(transaction):
    description = transaction.description.lower()
    logger.info(f"Description for transaction ID: {transaction.external_id}: {description}")
    return description

def find_keyword(description):
    try:
        matched_keyword = Keyword.objects.search_text(description).first()
        if matched_keyword:
            return matched_keyword
    except Exception as e:
        logger.error(f"Error during keyword search: {str(e)}")
    return None


def handle_enrichment_error(transaction_id, error):
    logger.error(f"Error during enrichment for transaction ID: {transaction_id}: {str(error)}")
    logger.error("Traceback:", exc_info=True)  # This logs the stack trace

def calculate_metrics(enriched_transactions, total_transactions_received, total_keyword_matches):
    successful_categorizations = sum(1 for tx in enriched_transactions if tx.category is not None)
    successful_identifications = sum(1 for tx in enriched_transactions if tx.commerce is not None)
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

    matched_keyword = find_keyword(description)
    commerce = None
    category = None

    if matched_keyword:
        commerce = matched_keyword.merchant_id
        category = matched_keyword.merchant_id.category if matched_keyword.merchant_id else None

    # Prepare the enriched data dictionary without saving the transaction
    enriched_data = get_enriched_data(transaction, merchant_id=commerce, category_id=category)

    logger.info(f"Enrichment completed for transaction ID: {transaction.external_id}")
    return enriched_data

def enrich_transactions(transactions):
    total_transactions_received = len(transactions)
    total_keyword_matches = 0
    enriched_transaction_docs = []

    for transaction in transactions:
        try:
            # Enrich the transaction and get the data as a dictionary
            enriched_data = enrich_transaction(transaction)

            # Prepare the Transaction object for bulk insertion
            transaction_doc = Transaction(
                external_id=UUID(enriched_data['external_id']),
                description=enriched_data['description'],
                amount=enriched_data['amount'],
                date=enriched_data['date'],
                category=enriched_data['category'],
                commerce=enriched_data['commerce'],
                updated_at=datetime.utcnow()
            )

            enriched_transaction_docs.append(transaction_doc)

            # Count successful keyword matches
            if enriched_data['category'] or enriched_data['commerce']:
                total_keyword_matches += 1

        except Exception as e:
            handle_enrichment_error(transaction.external_id, e)

    # Bulk insert enriched transactions
    if enriched_transaction_docs:
        try:
            Transaction.objects.insert(enriched_transaction_docs, load_bulk=False)
            logger.info("Bulk insert of enriched transactions completed successfully.")
        except BulkWriteError as bwe:
            logger.error(f"Bulk write error: {bwe.details}")

    # Calculate and return metrics
    metrics = calculate_metrics(enriched_transaction_docs, total_transactions_received, total_keyword_matches)
    return metrics