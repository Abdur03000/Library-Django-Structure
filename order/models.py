from sqlalchemy import Column, Integer, ForeignKey, Date, Float, String
from sqlalchemy.orm import relationship
from Library.db.database import Base  


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    rent_start_date = Column(Date)
    rent_end_date = Column(Date)
    total_rent = Column(Float)

    student = relationship("Student", back_populates="orders")
    book = relationship("Book", back_populates="orders")
    