from ..models.category import Category

def create_category(data):
    category = Category(**data)
    category.save()
    return category

def get_all_categories():
    return list(Category.objects.all())

def get_category_by_id(category_id):
    return Category.objects(id=category_id).first()

def update_category(category_id, data):
    category = get_category_by_id(category_id)
    if category:
        category.update(**data)
    return category

def delete_category(category_id):
    category = get_category_by_id(category_id)
    if category:
        category.delete()
    return category
