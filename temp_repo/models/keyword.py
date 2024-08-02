from mongoengine import Document, UUIDField, StringField, ReferenceField
import uuid

class Keyword(Document):
    keyword = StringField(required=True, max_length=255)
    merchant_id = ReferenceField('Commerce', required=True)

    meta = {'collection': 'keywords'}
