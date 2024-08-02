from mongoengine import Document, UUIDField, StringField, DecimalField, DateField, DateTimeField, ReferenceField
import uuid
from datetime import datetime

class Transaction(Document):
    id = UUIDField(primary_key=True, binary=False, required=True, default=uuid.uuid4)
    description = StringField(required=True, max_length=255)
    amount = DecimalField(required=True, null=True)
    date = DateField(required=True, null=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    category_id = ReferenceField('Category', null=True)
    commerce_id = ReferenceField('Commerce', null=True)