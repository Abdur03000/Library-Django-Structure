from fastapi import Depends
from sqlalchemy.orm import Session

from db.database import get_db
from student.repositories import StudentRepository  
from book.repositories import  BookRepository
from order.repositories import OrderRepository

def get_book_repository(db: Session = Depends(get_db)) -> BookRepository:
    return BookRepository(db)


def get_student_repository(db: Session = Depends(get_db)) -> StudentRepository:
    return StudentRepository(db)


def get_order_repository(db: Session = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)


def get_repository(repo_class):
    def _get_repo(session: Session = Depends(get_db)):
        return repo_class(session)
    return _get_repo
