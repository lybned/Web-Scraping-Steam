import mysql.connector
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float
# Define the base class for the model
Base = declarative_base()

# Define the table as a Python class
class Product(Base):
    __tablename__ = 'products'
    
    # Define columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255))
    Published_Date = Column(String(255))
    Original_Price = Column(Float)
    Discount_Percentage = Column(Float)
    Discount_Price = Column(Float)
    Rating = Column(String(255))
    Review_Rating = Column(String(255))
    Reviews_Numbers = Column(Integer)
    Since_Release = Column(Integer)
    Positive = Column(Float)
    Year = Column(Integer)
    Month = Column(Integer)
    Day = Column(Integer)
