from mongoengine import Document, UUIDField, StringField, DecimalField, DateField, DateTimeField, ValidationError, ReferenceField
import uuid
from datetime import datetime

class Transaction(Document):
    external_id = UUIDField(binary=False, default=uuid.uuid4, required=True)
    description = StringField(required=True, max_length=255)
    amount = DecimalField(required=True, precision=2, null=True)
    date = DateField(required=True, null=True)  # Date of the transaction
    category = ReferenceField('Category', null=True)  # Reference to Category
    commerce = ReferenceField('Commerce', null=True)  # Reference to Commerce

    category_type = StringField(max_length=10, choices=['income', 'expense'], null=True)
    created_at = DateTimeField(default=datetime.utcnow, required=True)
    updated_at = DateTimeField(default=datetime.utcnow, required=True)

    meta = {
        'indexes': [
            {'fields': ['-created_at']}  # Index for ordering by creation date
        ],
        'collection': 'transactions'
    }

    def clean(self):
        # Validate positive amount and future date
        if self.amount is None or self.amount == 0:
            raise ValidationError("Amount cannot be zero.")
        if self.date and self.date > datetime.utcnow().date():
            raise ValidationError("Transaction date cannot be in the future.")
        super().clean()

    def save(self, *args, **kwargs):
        # Set updated_at and category_type on save
        self.updated_at = datetime.utcnow()
        self.category_type = 'income' if self.amount > 0 else 'expense'
        return super(Transaction, self).save(*args, **kwargs)