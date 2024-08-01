from ..models.commerce import Commerce

def create_commerce(data):
    commerce = Commerce(**data)
    commerce.save()
    return commerce

def get_all_commerces():
    return list(Commerce.objects.all())

def get_commerce_by_id(commerce_id):
    return Commerce.objects(id=commerce_id).first()

def update_commerce(commerce_id, data):
    commerce = get_commerce_by_id(commerce_id)
    if commerce:
        commerce.update(**data)
    return commerce

def delete_commerce(commerce_id):
    commerce = get_commerce_by_id(commerce_id)
    if commerce:
        commerce.delete()
    return commerce
