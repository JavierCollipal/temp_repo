from ..models.keyword import Keyword

def create_keyword(data):
    keyword = Keyword(**data)
    keyword.save()
    return keyword

def get_all_keywords():
    return list(Keyword.objects.all())

def get_keyword_by_id(keyword_id):
    return Keyword.objects(id=keyword_id).first()

def update_keyword(keyword_id, data):
    keyword = get_keyword_by_id(keyword_id)
    if keyword:
        keyword.update(**data)
    return keyword

def delete_keyword(keyword_id):
    keyword = get_keyword_by_id(keyword_id)
    if keyword:
        keyword.delete()
    return keyword
