from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List
from Library.dependencies.service import get_book_service, get_order_service, get_student_service
from student.schmeas import Student, StudentCreate, StudentUpdate
from book.schmeas import Book, BookCreate, BookUpdate
from order.schmeas import OrderCreate,Order,OrderUpdate
from order.services import OrderService
from student.services import StudentService
from book.services import BookService
from Library.resources import strings

# Initialize routers without prefix (prefixes will be added in main/api_router file)
books_router = APIRouter(tags=["Books"])
orders_router = APIRouter(tags=["Orders"])
students_router = APIRouter(tags=["Students"])


# ------------------ Orders Endpoints ------------------
@orders_router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, service: OrderService = Depends(get_order_service)):
    created_order = service.create_order(order)
    return JSONResponse(
        content={"message": "Order created successfully", "order": created_order.dict()},
        status_code=status.HTTP_201_CREATED
    )

@orders_router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, service: OrderService = Depends(get_order_service)):
    db_order = service.get_order(order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail=strings.ORDER_NOT_FOUND)
    return db_order

@orders_router.get("/", response_model=List[Order])
def get_orders(skip: int = 0, limit: int = 100, service: OrderService = Depends(get_order_service)):
    return service.get_all_orders()

@orders_router.put("/{order_id}", response_model=Order)
def update_order(order_id: int, order: OrderUpdate, service: OrderService = Depends(get_order_service)):
    db_order = service.get_order(order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail=strings.ORDER_NOT_FOUND)
    updated_order = service.update_order(order_id, order)
    return JSONResponse(
        content={"message": "Order updated successfully", "order": updated_order.dict()},
        status_code=status.HTTP_200_OK
    )

@orders_router.delete("/{order_id}")
def delete_order(order_id: int, service: OrderService = Depends(get_order_service)):
    result = service.delete_order(order_id)
    if not result:
        return JSONResponse(
            content={"message": "Order not found or already deleted"},
            status_code=404
        )
    return JSONResponse(
        content={"message": "Order deleted successfully"},
        status_code=200
    )

@orders_router.post("/{order_id}/return", response_model=Order)
def return_order(order_id: int, service: OrderService = Depends(get_order_service)):
    db_order = service.get_order(order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail=strings.ORDER_NOT_FOUND)
    if db_order.return_date is not None:
        return JSONResponse(
            content={"message": "Book already returned"},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    returned_order = service.return_order(order_id)
    return JSONResponse(
        content={"message": "Book returned successfully", "order": returned_order.dict()},
        status_code=status.HTTP_200_OK
    )
