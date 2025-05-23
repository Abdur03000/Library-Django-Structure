from sqlalchemy.orm import Session
from book.models import Book as BookModel
from book.schmeas import BookCreate, BookUpdate
from datetime import date
from student.models  import Student as StudentModel
from .schmeas import StudentCreate, StudentUpdate
from order.models import Order as OrderModel
from order.schmeas import OrderCreate, OrderUpdate
from fastapi import HTTPException, status

class BaseRepository:
    """
    Base repository that holds the DB session.
    """
    def __init__(self, session: Session):
        self.session = session


class StudentRepository(BaseRepository):

    def create(self, student_in: StudentCreate) -> StudentModel:
        # Check if email already exists
        existing_email = self.session.query(StudentModel).filter(StudentModel.email == student_in.email).first()
        if existing_email:
            raise ValueError(f"Student with email '{student_in.email}' already exists.")
        
        # Check if name already exists
        existing_name = self.session.query(StudentModel).filter(StudentModel.name == student_in.name).first()
        if existing_name:
            raise ValueError(f"Student with name '{student_in.name}' already exists.")

        student = StudentModel(
            name=student_in.name,
            email=student_in.email,
            photo=student_in.photo,
        )
        self.session.add(student)
        self.session.commit()
        self.session.refresh(student)
        return student

    def get_by_id(self, student_id: int):  
        return self.session.query(StudentModel).filter(StudentModel.id == student_id).first()

    def update(self, student_id: int, student_in: StudentUpdate):
        student = self.get_by_id(student_id)
        if not student:
            return None
        for field, value in student_in.dict(exclude_unset=True).items():
            setattr(student, field, value)
        self.session.commit()
        self.session.refresh(student)
        return student

    def delete(self, order_id: int):
        order = self.get_by_id(order_id)
        if not order:
            return None
        self.session.delete(order)
        self.session.commit()
        return order


