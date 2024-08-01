from ..models.transaction import Transaction


def list_transactions():
    return Transaction.objects.all()

def create_transaction(data):
    transaction = Transaction(**data)
    transaction.save()
    return transaction

def create_transactions(data):
    transactions = [Transaction(**item) for item in data]
    Transaction.objects.insert(transactions)
