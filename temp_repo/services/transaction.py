from ..models.transaction import Transaction


def list_transactions():
    return Transaction.objects.all()

def create_transaction(data):
    transaction = Transaction(**data)
    transaction.save()
    return transaction

def create_transactions(data, max_batch_size=500):
    # Determine actual batch size based on the data length and max_batch_size
    actual_batch_size = min(max_batch_size, len(data))
    transactions = [Transaction(**item) for item in data]
    for i in range(0, len(transactions), actual_batch_size):
        Transaction.objects.insert(transactions[i:i+actual_batch_size])
