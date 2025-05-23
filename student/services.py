from fastapi import Depends
from book.repositories import BookRepository
from book.schmeas import BookCreate, BookUpdate
from fastapi import Depends
from Library.utils.services import BaseService
from Library.dependencies.repository import get_repository
from order.repositories import OrderRepository
from book.repositories import BookRepository
from order.schmeas import Order, OrderCreate, OrderUpdate
from datetime import date
from fastapi import Depends
from .repositories import StudentRepository
from .schmeas import StudentCreate, StudentUpdate


class BaseService:
    def __init__(self, repository):
        self.repository = repository

def get_repository(repo_class):
    
    pass

class StudentService(BaseService):
    def __init__(self, student_repo: StudentRepository = Depends(get_repository(StudentRepository))):
        self.student_repo = student_repo

    def create_student(self, student: StudentCreate):
        return self.student_repo.create(student)

    def get_student(self, student_id: int):
        return self.student_repo.get_by_id(student_id)  

    def update_student(self, student_id: int, student_data: StudentUpdate):
        return self.student_repo.update(student_id, student_data)

    def delete_student(self, student_id: int):
        return self.student_repo.delete(student_id)

    def get_all_students(self):
        return self.student_repo.get_all()  
