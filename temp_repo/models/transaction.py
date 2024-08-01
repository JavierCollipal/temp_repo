# temp_repo/models/transaction.py
from mongoengine import Document, UUIDField, StringField, DecimalField, DateField
import uuid

class Transaction(Document):
    id = UUIDField(binary=False, required=True, default=uuid.uuid4, primary_key=True)
    description = StringField(required=True, max_length=255)
    amount = DecimalField(required=True)
    date = DateField(required=True)

    meta = {'collection': 'transactions'}
