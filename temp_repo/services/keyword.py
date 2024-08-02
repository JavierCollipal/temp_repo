from ..models.keyword import Keyword
from bson import ObjectId
from mongoengine import ValidationError
def create_keyword(data):
    """
    Create a new keyword.
    :param data: Dictionary containing the keyword data.
    :return: The created Keyword object.
    """
    # Ensure 'id' is not included in the data
    if 'id' in data:
        del data['id']
    keyword = Keyword(**data)
    keyword.save()
    return keyword

def get_all_keywords():
    """
    Retrieve all keywords from the database.
    :return: List of Keyword objects.
    """
    return list(Keyword.objects.all())

def get_keyword_by_id(keyword_id):
    """
    Retrieve a single keyword by its ID.
    :param keyword_id: The ID of the keyword to retrieve.
    :return: The Keyword object if found, otherwise None.
    """
    # Convert keyword_id to ObjectId if necessary
    try:
        if not isinstance(keyword_id, ObjectId):
            keyword_id = ObjectId(keyword_id)
    except Exception as e:
        raise ValueError("Invalid ID format") from e

    return Keyword.objects(id=keyword_id).first()

def update_keyword(keyword_id, data):
    """
    Update an existing keyword with the given data.
    :param keyword_id: The ID of the keyword to update.
    :param data: Dictionary containing the updated keyword data.
    :return: The updated Keyword object if found, otherwise None.
    """
    keyword = get_keyword_by_id(keyword_id)
    if keyword:
        # Ensure merchant_id is converted to ObjectId if present in data
        if 'merchant_id' in data:
            try:
                data['merchant_id'] = ObjectId(data['merchant_id'])
            except Exception as e:
                raise ValueError("Invalid merchant_id format") from e

        try:
            keyword.update(**data)
            keyword.reload()
            return keyword
        except ValidationError as e:
            raise ValueError(f"Validation Error: {e.message}") from e
    else:
        return None

def delete_keyword(keyword_id):
    """
    Delete a keyword by its ID.
    :param keyword_id: The ID of the keyword to delete.
    :return: The deleted Keyword object if found, otherwise None.
    """
    keyword = get_keyword_by_id(keyword_id)
    if keyword:
        keyword.delete()
    return keyword