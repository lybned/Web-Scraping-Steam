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
conn = mysql.connector.connect(user=user, password=password, host=host, port=port)
cursor = conn.cursor()





# Create a new database
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
print("Database created.")


# Use the specified database
cursor.execute(f"USE {database}")

# Create a table with all columns as strings
cursor.execute("""
CREATE TABLE IF NOT EXISTS Vuls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Published_Date VARCHAR(255),
    Original_Price VARCHAR(255),
    Discount_Percentage FLOAT,
    Discount_Price FLOAT,
    Rating VARCHAR(255),
    Review_Rating VARCHAR(500),
    Reviews_Numbers INT,
    Since_Release INT,
    Positive FLOAT,
    Year INT,
    Month INT,
    Day INT
)
""")
print("Table created.")

# Clean up
cursor.close()
conn.close()



