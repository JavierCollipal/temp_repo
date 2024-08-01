from mongoengine import Document, UUIDField, StringField, ReferenceField, URLField
import uuid

class Commerce(Document):
    id = UUIDField(binary=False, required=True, default=uuid.uuid4, primary_key=True)
    merchant_name = StringField(required=True, max_length=255)
    merchant_logo = URLField(required=False)
    category = ReferenceField('Category', required=True)

    meta = {'collection': 'commerces'}
