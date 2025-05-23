from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List

from Library.dependencies.service import get_book_service, get_order_service, get_student_service
from student.schmeas import Student, StudentCreate, StudentUpdate
from order.schmeas import Order, OrderCreate, OrderUpdate
from book.schmeas import  Book, BookCreate, BookUpdate
from book.services import BookService
from order.services import OrderService
from student.services import StudentService
from Library.resources import strings

# Initialize routers without prefix (prefixes will be added in main/api_router file)
books_router = APIRouter(tags=["Books"])
orders_router = APIRouter(tags=["Orders"])
students_router = APIRouter(tags=["Students"])


# ------------------ Students Endpoints ------------------
@students_router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, service: StudentService = Depends(get_student_service)):
    try:
        return service.create_student(student)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@students_router.get("/{student_id}", response_model=Student)
def get_student(student_id: int, service: StudentService = Depends(get_student_service)):
    db_student = service.get_student(student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail=strings.STUDENT_NOT_FOUND)
    return db_student

@students_router.get("/", response_model=List[Student])
def get_students(skip: int = 0, limit: int = 100, service: StudentService = Depends(get_student_service)):
    return service.get_all_students()

@students_router.put("/{student_id}", response_model=Student)
def update_student(student_id: int, student: StudentUpdate, service: StudentService = Depends(get_student_service)):
    db_student = service.get_student(student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail=strings.STUDENT_NOT_FOUND)
    return service.update_student(student_id, student)

@students_router.delete("/{student_id}", status_code=status.HTTP_200_OK)
def delete_student(student_id: int, service: StudentService = Depends(get_student_service)):
    db_student = service.get_student(student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail=strings.STUDENT_NOT_FOUND)
    service.delete_student(student_id)
    return {"message": "Student deleted successfully", "id": student_id}
