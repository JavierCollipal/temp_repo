from mongoengine import Document, UUIDField, StringField, DateTimeField
import uuid
from datetime import datetime

class Category(Document):
    external_id = UUIDField(binary=False, required=True, default=uuid.uuid4)
    name = StringField(required=True, max_length=255)
    type = StringField(required=True, choices=['expense', 'income'])
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'categories',
    }

    def save(self, *args, **kwargs):
        # Update updated_at timestamp on every save
        self.updated_at = datetime.utcnow()
        return super(Category, self).save(*args, **kwargs)