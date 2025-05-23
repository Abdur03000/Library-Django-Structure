from sqlalchemy import Column, Integer, ForeignKey, Date, Float, String
from sqlalchemy.orm import relationship
from Library.db.database import Base  

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String, nullable=True)
    cover_image = Column(String, nullable=True)

    orders = relationship("Order", back_populates="book", cascade="all, delete")
    