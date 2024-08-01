from ..models.transaction import Transaction

def list_transactions():
    return Transaction.objects.all()

def create_transaction(data):
    transaction = Transaction(**data)
    transaction.save()
    return transaction