from mongoengine import Document, UUIDField, StringField, ReferenceField, DateTimeField
import uuid
from datetime import datetime


class Keyword(Document):
    external_id = UUIDField(binary=False, required=True, default=uuid.uuid4)
    keyword = StringField(required=True, max_length=255)
    merchant_id = ReferenceField('Commerce', required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'keywords',
        'indexes': [
            {
                'fields': ['$keyword'],
                'default_language': 'none',
                'weights': {'keyword': 10}
            }
        ]
    }

    def save(self, *args, **kwargs):
        # Update updated_at timestamp on every save
        self.updated_at = datetime.utcnow()
        return super(Keyword, self).save(*args, **kwargs)