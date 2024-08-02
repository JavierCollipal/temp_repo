from mongoengine import Document, UUIDField, StringField, ReferenceField, URLField, DateTimeField
import uuid
from datetime import datetime
class Commerce(Document):
    external_id = UUIDField(binary=False, required=True, default=uuid.uuid4)

    merchant_name = StringField(required=True, max_length=255)
    merchant_logo = URLField(required=False)
    category = ReferenceField('Category', required=False, null=True) 
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)


    meta = {'collection': 'commerces'}

    def save(self, *args, **kwargs):
        # Update updated_at timestamp on every save
        self.updated_at = datetime.utcnow()
        return super(Commerce, self).save(*args, **kwargs)