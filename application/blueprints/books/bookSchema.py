from application.models import Book
from application.extensions import ma



class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book

book_schema = BookSchema()
books_schema = BookSchema(many=True)