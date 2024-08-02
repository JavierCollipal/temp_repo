from ..models.category import Category
from bson import ObjectId

def create_category(data):
    """
    Create a new category.
    :param data: Dictionary containing the category data.
    :return: The created Category object.
    """
    category = Category(**data)
    category.save()
    return category

def get_all_categories():
    """
    Retrieve all categories from the database.
    :return: List of Category objects.
    """
    return list(Category.objects.all())

def get_category_by_id(category_id):
    """
    Retrieve a single category by its ID.
    :param category_id: The ID of the category to retrieve.
    :return: The Category object if found, otherwise None.
    """
    try:
        if not isinstance(category_id, ObjectId):
            category_id = ObjectId(category_id)
    except Exception as e:
        raise ValueError("Invalid ID format") from e

    return Category.objects(id=category_id).first()

def update_category(category_id, data):
    """
    Update an existing category with the given data.
    :param category_id: The ID of the category to update.
    :param data: Dictionary containing the updated category data.
    :return: The updated Category object if found, otherwise None.
    """
    category = get_category_by_id(category_id)
    if category:
        try:
            category.update(**data)
            category.reload()
            return category
        except Exception as e:
            raise ValueError(f"Error updating category: {e}") from e
    else:
        return None

def delete_category(category_id):
    """
    Delete a category by its ID.
    :param category_id: The ID of the category to delete.
    :return: The deleted Category object if found, otherwise None.
    """
    category = get_category_by_id(category_id)
    if category:
        category.delete()
    return category