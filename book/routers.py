from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List
from Library.dependencies.service import get_book_service, get_order_service, get_student_service
from student.schmeas  import   Student, StudentCreate, StudentUpdate
from book.schmeas import Book, BookCreate, BookUpdate
from order.schmeas import Order, OrderCreate, OrderUpdate
from order.services import OrderService
from book.services import BookService
from Library.resources import strings
from student.services import StudentService

# Initialize routers without prefix (prefixes will be added in main/api_router file)
books_router = APIRouter(tags=["Books"])
orders_router = APIRouter(tags=["Orders"])
students_router = APIRouter(tags=["Students"])

# ------------------ Books Endpoints ------------------
@books_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, service: BookService = Depends(get_book_service)):
    try:
        return service.create_book(book)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@books_router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, service: BookService = Depends(get_book_service)):
    db_book = service.get_book(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail=strings.BOOK_NOT_FOUND)
    return db_book

@books_router.get("/", response_model=List[Book])
def get_books(skip: int = 0, limit: int = 100, service: BookService = Depends(get_book_service)):
    return service.get_all_books()

@books_router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookUpdate, service: BookService = Depends(get_book_service)):
    db_book = service.get_book(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail=strings.BOOK_NOT_FOUND)
    return service.update_book(book_id, book)

@books_router.delete("/{book_id}")
def delete_book(book_id: int, service: BookService = Depends(get_book_service)):
    deleted_book = service.delete_book(book_id)
    if not deleted_book:
        raise HTTPException(status_code=404, detail=f"No book found with ID {book_id}")
    return {"message": "Book deleted successfully", "id": book_id}
