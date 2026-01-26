from .models import Authors


def create_author_logic(full_name, bio, image=None):
    return Authors.objects.create(full_name=full_name, bio=bio, image=image)


def get_author_data_by_id(author_id):
    try:
        author = Authors.objects.get(id=author_id)
        return {
            "id": author.id,
            "full_name": author.full_name,
            "bio": author.bio
        }
    except Authors.DoesNotExist:
        return None


def get_authors_by_ids(author_ids):
    authors = Authors.objects.filter(id__in=author_ids)
    return {a.id: a.full_name for a in authors}