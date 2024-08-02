from mongoengine import Document, UUIDField, StringField
import uuid

class Category(Document):
    name = StringField(required=True, max_length=255)
    type = StringField(required=True, choices=['expense', 'income'])

    meta = {'collection': 'categories'}