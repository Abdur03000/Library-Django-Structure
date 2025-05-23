from pydantic import BaseModel
from datetime import date
from typing import Optional

class OrderCreate(BaseModel):
    student_id: int
    book_id: int
    return_date: date  # User only provides return date

class OrderUpdate(BaseModel):
    return_date: date

class Order(BaseModel):
    id: int
    student_id: int
    book_id: int
    issue_date: date
    return_date: date
    total_days: int
    total_rent: float
    student_photo: Optional[str]
    book_cover: Optional[str]

    model_config = {
    "from_attributes": True  
}
