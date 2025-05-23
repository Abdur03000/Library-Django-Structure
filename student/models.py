from sqlalchemy import Column, Integer, ForeignKey, Date, Float, String
from sqlalchemy.orm import relationship
from Library.db.database import Base  


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    photo = Column(String, nullable=True)

    # example: one-to-many relationship to orders (optional)
    orders = relationship("Order", back_populates="student")