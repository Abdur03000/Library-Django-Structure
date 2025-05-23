from fastapi import APIRouter

from book.routers import books_router 
from student.routers import students_router 
from order.routers import orders_router 

api_router = APIRouter()

api_router.include_router(books_router, prefix="/books", tags=["Books"])
api_router.include_router(students_router, prefix="/students", tags=["Students"])
api_router.include_router(orders_router, prefix="/orders", tags=["Orders"])
