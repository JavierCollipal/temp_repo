import logging
from ..models.transaction import Transaction
from ..models.commerce import Commerce
from ..models.keyword import Keyword
from mongoengine.errors import DoesNotExist

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
        'id': str(transaction.id),
        'description': transaction.description,
        'amount': transaction.amount,
        'date': transaction.date,
        'category_id': category_id,
        'commerce_id': merchant_id,
    }

def log_description(transaction):
    description = transaction.description.lower()
    logger.info(f"Description for transaction ID: {transaction.id}: {description}")
    return description

def find_keyword(description):
    try:
        matched_keyword = Keyword.objects.search_text(description).first()
        if matched_keyword:
            logger.debug(f"Matched keyword: {matched_keyword.keyword}")
            return matched_keyword
    except Exception as e:
        logger.error(f"Error during keyword search: {str(e)}")
    return None

def fetch_commerce_by_id(merchant_id):
    try:
        commerce = Commerce.objects.get(id=merchant_id)
        logger.info(f"Found commerce: {commerce.merchant_name} for merchant_id: {merchant_id}")
        return commerce
    except DoesNotExist:
        logger.warning(f"Commerce not found for merchant_id: {merchant_id}")
        return None

def handle_enrichment_error(transaction_id, error):
    logger.error(f"Error during enrichment for transaction ID: {transaction_id}: {str(error)}")

def calculate_metrics(enriched_transactions, total_transactions_received, total_keyword_matches):
    successful_categorizations = sum(1 for tx in enriched_transactions if tx['category_id'])
    successful_identifications = sum(1 for tx in enriched_transactions if tx['commerce_id'])
    match_keyword_rate = (total_keyword_matches / total_transactions_received) * 100

    categorization_rate = (successful_categorizations / total_transactions_received) * 100
    merchant_identification_rate = (successful_identifications / total_transactions_received) * 100

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
    logger.info(f"Starting enrichment for transaction ID: {transaction.id}")
    description = log_description(transaction)

    matched_keyword = find_keyword(description)
    if matched_keyword:
        merchant_id = matched_keyword.merchant_id
        
        # Attempt to fetch commerce details and log result
        commerce = fetch_commerce_by_id(merchant_id)
        if commerce:
            logger.info(f"Enrichment successful for transaction ID: {transaction.id} with commerce {commerce.merchant_name}")
        else:
            logger.warning(f"No commerce found for merchant_id: {merchant_id}")

        category_id = matched_keyword.category_id if matched_keyword else None
        return get_enriched_data(transaction, merchant_id=merchant_id, category_id=category_id)

    # If no keyword is matched, return transaction data without enrichment
    return get_enriched_data(transaction)

def enrich_transactions(transactions):
    total_transactions_received = len(transactions)
    total_keyword_matches = 0
    enriched_transactions = []

    for transaction in transactions:
        try:
            description = log_description(transaction)
            matched_keyword = find_keyword(description)

            if matched_keyword:
                total_keyword_matches += 1
            enriched_data = enrich_transaction(transaction)
            

            enriched_transactions.append(enriched_data)
        except Exception as e:
            handle_enrichment_error(transaction.id, e)

    metrics = calculate_metrics(enriched_transactions, total_transactions_received, total_keyword_matches)
    return metrics 