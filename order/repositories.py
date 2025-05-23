
from sqlalchemy.orm import Session
from book.models import Book as BookModel
from book.schmeas import BookCreate, BookUpdate
from datetime import date
from student.models import Student as StudentModel
from student.schmeas import StudentCreate, StudentUpdate
from order.models import Order as OrderModel
from .schmeas import OrderCreate, OrderUpdate
from fastapi import HTTPException, status

class BaseRepository:
    """
    Base repository that holds the DB session.
    """
    def __init__(self, session: Session):
        self.session = session


class OrderRepository(BaseRepository):



    def create(self, order_in: OrderCreate) -> OrderModel:
        today = date.today()

        # Check if book is currently rented and not yet returned
        active_rental = (
            self.session.query(OrderModel)
            .filter(
                OrderModel.book_id == order_in.book_id,
                OrderModel.rent_end_date >= today
            )
            .first()
        )
        if active_rental:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book is already rented and not yet returned."
            )

        rent_start_date = today
        rent_end_date = order_in.return_date

        total_days = (rent_end_date - rent_start_date).days + 1
        if total_days < 1:
            total_days = 1

        total_rent = total_days * 30  # or your rent calculation logic

        order = OrderModel(
            student_id=order_in.student_id,
            book_id=order_in.book_id,
            rent_start_date=rent_start_date,
            rent_end_date=rent_end_date,
            total_rent=total_rent,
        )
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order


    def get_all(self):
        return self.session.query(OrderModel).all()

    def get_by_id(self, order_id: int):
        return self.session.query(OrderModel).filter(OrderModel.id == order_id).first()

    def get_by_student_id(self, student_id: int):
        return self.session.query(OrderModel).filter(OrderModel.student_id == student_id).all()

    def update(self, order_id: int, order_in: OrderUpdate):
        order = self.get_by_id(order_id)
        if not order:
            return None
        for field, value in order_in.dict(exclude_unset=True).items():
            setattr(order, field, value)
        self.session.commit()
        self.session.refresh(order)
        return order

    def delete(self, order_id: int):
        order = self.get_by_id(order_id)
        if not order:
            return None
        self.session.delete(order)
        self.session.commit()
        return order
