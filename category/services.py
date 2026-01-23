from .models import Category


def create_category_logic(name, slug):
    category = Category.objects.create(
        name=name,
        slug=slug
    )
    return category



def get_category_data_by_id(category_id):
    try:
        category = Category.objects.get(id=category_id)
        return {"id": category.id, "name": category.name, "slug": category.slug}
    except Category.DoesNotExist:
        return None


def get_categories_by_ids(category_ids):
    # Bazadan barcha kerakli kategoriyalarni bittada filtrlab olamiz
    categories = Category.objects.filter(id__in=category_ids)

    # Natijani lug'at (dict) ko'rinishida qaytaramiz: {id: name}
    # Bu orqali Book moduli ID bo'yicha nomni tez topib oladi
    return {c.id: c.name for c in categories}