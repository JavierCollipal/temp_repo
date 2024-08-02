from mongoengine import Document, StringField, DecimalField, DateField, DateTimeField
from datetime import datetime

class Transaction(Document):
    description = StringField(required=True, max_length=255)
    amount = DecimalField(required=True)
    date = DateField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'transactions',
    }

    def save(self, *args, **kwargs):
        # If it's a new document, set created_at
        if not self.created_at:
            self.created_at = datetime.utcnow()
        # Always update updated_at to current time
        self.updated_at = datetime.utcnow()
        return super(Transaction, self).save(*args, **kwargs)
