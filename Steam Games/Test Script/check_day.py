'''
from datetime import datetime

# Get the current date
current_date = datetime.now().date()
print(current_date)
print(current_date.year)



import mysql.connector
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from product import Product
Base = declarative_base()
'''
import mysql.connector
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from product import Product
Base = declarative_base()
'''
# Define the base class for the model
Base = declarative_base()

# Define the table as a Python class
class Product(Base):
    __tablename__ = 'products'
    
    # Define columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255))
    Published_Date = Column(String(255))
    Original_Price = Column(String(255))
    Discount_Percentage = Column(String(255))
    Discount_Price = Column(String(255))
    Rating = Column(String(255))
    Review_Rating = Column(String(255))
    Reviews_Numbers = Column(String(255))
    Year = Column(Integer)
    Month = Column(Integer)
    Day = Column(Integer)
    '''

# Load environment variables from .env file
load_dotenv()

# Retrieve values from environment variables
host = os.getenv("MYSQL_HOST")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
port = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DATABASE")

# Connect to MySQL without specifying a database
'''
conn = mysql.connector.connect(user=user, password=password, host=host, port=port)
cursor = conn.cursor()

cursor.execute(f"USE {database}")

cursor.execute("TRUNCATE TABLE products")
# Clean up
cursor.close()
conn.close()
'''

from datetime import datetime

# Input date string
date_str = "12 Aug, 2016"

# Convert to datetime object
date_obj = datetime.strptime(date_str, "%d %b, %Y").date()

# Get today's date
today = datetime.now().date()

# Calculate difference in days
day_difference = (today - date_obj).days

print(f"Difference in days: {day_difference}")



