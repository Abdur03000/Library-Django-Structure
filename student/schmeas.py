from pydantic import BaseModel
from typing import Optional


class StudentBase(BaseModel):
    name: str
    email: str


class StudentCreate(StudentBase):
    photo: Optional[str]


class StudentUpdate(StudentBase):
    photo: Optional[str]


class Student(StudentBase):
    id: int
    photo: Optional[str]

    model_config = {
        "from_attributes": True
    }
