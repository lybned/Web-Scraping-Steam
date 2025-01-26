import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve values from environment variables
host = os.getenv("MYSQL_HOST")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
port = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DATABASE")


# Connect to the MySQL server
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    port=port
)

cursor = connection.cursor()

# Create a new database
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
print("Database created.")


# Use the specified database
cursor.execute(f"USE {database}")

# Create a table with all columns as strings
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Published_Date VARCHAR(255),
    Original_Price VARCHAR(255),
    Discount_Percentage VARCHAR(255),
    Discount_Price VARCHAR(255),
    Rating VARCHAR(255),
    Review_Rating VARCHAR(255),
    Reviews_Numbers VARCHAR(255)
)
""")
print("Table created.")

# Clean up
cursor.close()
connection.close()

