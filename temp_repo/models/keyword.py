from mongoengine import Document, UUIDField, StringField, ReferenceField
import uuid

class Keyword(Document):
    external_id = UUIDField(binary=False, required=True, default=uuid.uuid4)
    keyword = StringField(required=True, max_length=255)
    merchant_id = ReferenceField('Commerce', required=True)

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