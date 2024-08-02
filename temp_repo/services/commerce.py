from ..models.commerce import Commerce
from bson import ObjectId

def create_commerce(data):
    commerce = Commerce(**data)
    commerce.save()
    return commerce

def get_all_commerces():
    return list(Commerce.objects.all())

def get_commerce_by_id(commerce_id):
    try:
        if not isinstance(commerce_id, ObjectId):
            commerce_id = ObjectId(commerce_id)
    except Exception as e:
        raise ValueError("Invalid ID format") from e
    return Commerce.objects(id=commerce_id).first()


def update_commerce(commerce_id, data):
    try:
        # Ensure category is an ObjectId
        if 'category' in data and not isinstance(data['category'], ObjectId):
            data['category'] = ObjectId(data['category'])
        
        commerce = Commerce.objects.get(id=commerce_id)
        commerce.update(**data)
        return commerce
    except Exception as e:
        raise ValueError(f"Error updating commerce: {e}") from e


def delete_commerce(commerce_id):
    commerce = get_commerce_by_id(commerce_id)
    if commerce:
        commerce.delete()
    return commerce
