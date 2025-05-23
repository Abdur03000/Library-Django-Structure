from sqlalchemy.orm import Session
from book.models import Book as BookModel
from book.schmeas import BookCreate, BookUpdate
from datetime import date
from student.models import Student as StudentModel
from student.schmeas import StudentCreate, StudentUpdate
from order.models import Order as OrderModel
from order.schmeas import OrderCreate, OrderUpdate
from fastapi import HTTPException, status

class BaseRepository:
    """
    Base repository that holds the DB session.
    """
    def __init__(self, session: Session):
        self.session = session


class BookRepository(BaseRepository):

    def create(self, book_in: BookCreate) -> BookModel:
        # Check if book title already exists
        existing_book = self.session.query(BookModel).filter(BookModel.title == book_in.title).first()
        if existing_book:
            raise ValueError(f"Book with title '{book_in.title}' already exists.")

        book = BookModel(
            title=book_in.title,
            author=book_in.author,
            description=book_in.description,
            cover_image=book_in.cover_image,
        )
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book


    def get_all(self):
        return self.session.query(BookModel).all()

    def get_by_id(self, book_id: int):
        return self.session.query(BookModel).filter(BookModel.id == book_id).first()

    def update(self, book_id: int, book_in: BookUpdate):
        book = self.get_by_id(book_id)
        if not book:
            return None
        for field, value in book_in.dict(exclude_unset=True).items():
            setattr(book, field, value)
        self.session.commit()
        self.session.refresh(book)
        return book

    def delete(self, book_id: int):
        book = self.get_by_id(book_id)
        if not book:
            return None
        self.session.delete(book)
        self.session.commit()
        return book
