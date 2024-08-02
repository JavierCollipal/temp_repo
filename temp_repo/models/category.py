from mongoengine import Document, UUIDField, StringField
import uuid
class Category(Document):
    external_id = UUIDField(binary=False, required=True, default=uuid.uuid4)

    name = StringField(required=True, max_length=255)
    type = StringField(required=True, choices=['expense', 'income'])

    meta = {'collection': 'categories'}