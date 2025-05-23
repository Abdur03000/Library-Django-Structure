from fastapi import Depends
from book.services import BookService
from student.services import StudentService
from order.services import OrderService

from dependencies.repository import (
    get_book_repository,
    get_student_repository,
    get_order_repository,
)


def get_book_service(book_repo=Depends(get_book_repository)) -> BookService:
    return BookService(book_repo)


def get_student_service(student_repo=Depends(get_student_repository)) -> StudentService:
    return StudentService(student_repo)


def get_order_service(order_repo=Depends(get_order_repository)) -> OrderService:
    return OrderService(order_repo)
