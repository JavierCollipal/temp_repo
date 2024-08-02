from mongoengine import Document, UUIDField, StringField, ReferenceField, URLField
import uuid

class Commerce(Document):
    merchant_name = StringField(required=True, max_length=255)
    merchant_logo = URLField(required=False)
    category = ReferenceField('Category', required=True)

    meta = {'collection': 'commerces'}
