from fastapi import Depends
from .repositories import BookRepository
from .schmeas import BookCreate, BookUpdate
from fastapi import Depends
from Library.utils.services import BaseService
from Library.dependencies.repository import get_repository
from order.repositories import OrderRepository
from book.repositories import BookRepository
from order.schmeas import Order, OrderCreate, OrderUpdate
from datetime import date
from fastapi import Depends
from student.repositories import StudentRepository
from student.schmeas import StudentCreate, StudentUpdate


class BaseService:
    def __init__(self, repository):
        self.repository = repository

def get_repository(repo_class):
    
    pass

class BookService(BaseService):
    def __init__(self, book_repo: BookRepository = Depends(get_repository(BookRepository))):
        super().__init__(book_repo)
        self.book_repo = book_repo

    def create_book(self, book: BookCreate):
        return self.book_repo.create(book)

    def get_book(self, book_id: int):
        return self.book_repo.get_by_id(book_id)  

    def update_book(self, book_id: int, book_data: BookUpdate):
        
        return self.book_repo.update(book_id, book_data)

    def delete_book(self, book_id: int):

        return self.book_repo.delete(book_id)  

    def get_all_books(self):
        return self.book_repo.get_all()  
