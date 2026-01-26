from .models import Book
from author.services import get_authors_by_ids
from category.services import get_categories_by_ids


def create_book_logic(name, title,  price, author_id, category_id, image=None):
    book = Book.objects.create(
        name=name, title=title, image=image,
        price=price, author_id=author_id, category_id=category_id
    )
    print("book", book)
    return book


def enrich_books_data(books):
    author_ids = [b.author_id for b in books]
    category_ids = [b.category_id for b in books]

    authors_map = get_authors_by_ids(author_ids)
    categories_map = get_categories_by_ids(category_ids)

    for book in books:
        book.author_name = authors_map.get(book.author_id, "Noma'lum")
        book.category_name = categories_map.get(book.category_id, "Ma'lumot yo'q")

    return books