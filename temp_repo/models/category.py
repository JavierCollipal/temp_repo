from mongoengine import Document, UUIDField, StringField
import uuid

class Category(Document):
    id = UUIDField(binary=False, required=True, default=uuid.uuid4, primary_key=True)
    name = StringField(required=True, max_length=255)
    type = StringField(required=True, choices=['expense', 'income'])

    meta = {'collection': 'categories'}