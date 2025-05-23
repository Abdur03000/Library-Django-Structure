from book.repositories import BookRepository
from book.schmeas import BookCreate, BookUpdate
from fastapi import Depends
from Library.utils.services import BaseService
from Library.dependencies.repository import get_repository
from order.repositories import OrderRepository
from book.repositories import BookRepository
from .schmeas import Order, OrderCreate, OrderUpdate
from datetime import date
from student.repositories import StudentRepository
from student.schmeas import StudentCreate, StudentUpdate


class BaseService:
    def __init__(self, repository):
        self.repository = repository

def get_repository(repo_class):
    
    pass

class OrderService(BaseService):
    def __init__(self, order_repo: OrderRepository = Depends(get_repository(OrderRepository))):
        self.order_repo = order_repo

    def _to_order_schema(self, db_order) -> Order:
        total_days = (db_order.rent_end_date - db_order.rent_start_date).days if db_order.rent_end_date and db_order.rent_start_date else 0
        return Order(
            id=db_order.id,
            student_id=db_order.student_id,
            book_id=db_order.book_id,
            issue_date=db_order.rent_start_date,
            return_date=db_order.rent_end_date,
            total_days=total_days,
            total_rent=db_order.total_rent,
            student_photo=db_order.student.photo if db_order.student else None,
            book_cover=db_order.book.cover_image if db_order.book else None,
        )

    def create_order(self, order: OrderCreate):
        db_order = self.order_repo.create(order)
        return self._to_order_schema(db_order)

    def get_order(self, order_id: int):
        db_order = self.order_repo.get_by_id(order_id)
        if not db_order:
            return None
        return self._to_order_schema(db_order)

    def update_order(self, order_id: int, order_data: OrderUpdate):
        db_order = self.order_repo.update(order_id, order_data)
        if not db_order:
            return None
        return self._to_order_schema(db_order)

    def get_all_orders(self):
        db_orders = self.order_repo.get_all()
        return [self._to_order_schema(order) for order in db_orders]

    def delete_order(self, order_id: int):
        return self.order_repo.delete(order_id)

    def return_order(self, order_id: int):
        db_order = self.order_repo.get_by_id(order_id)
        if not db_order:
            return None
        
        
        if db_order.rent_end_date and db_order.rent_end_date <= date.today():
        
            return self._to_order_schema(db_order)
        
        db_order.rent_end_date = date.today()
        total_days = (db_order.rent_end_date - db_order.rent_start_date).days + 1
        if total_days < 1:
            total_days = 1
        
        db_order.total_rent = total_days * 30  
        
        self.order_repo.session.commit()
        self.order_repo.session.refresh(db_order)
        
        return self._to_order_schema(db_order)