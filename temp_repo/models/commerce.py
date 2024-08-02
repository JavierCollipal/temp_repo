from mongoengine import Document, UUIDField, StringField, ReferenceField, URLField
import uuid

class Commerce(Document):
    external_id = UUIDField(binary=False, required=True, default=uuid.uuid4)

    merchant_name = StringField(required=True, max_length=255)
    merchant_logo = URLField(required=False)
    category = ReferenceField('Category', required=False, null=True) 


    meta = {'collection': 'commerces'}
