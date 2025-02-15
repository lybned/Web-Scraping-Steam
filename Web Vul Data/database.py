import mysql.connector
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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
    CVE_ID VARCHAR(255),
    Published_Date Date,
    Status VARCHAR(100),
    Description TEXT,
    Base_Severity VARCHAR(100),
    Exploitability_Score FLOAT,
    Impact_Score FLOAT,
    Base_Score FLOAT,
    Access_Vector VARCHAR(50),
    Access_Complexity VARCHAR(50),
    Authentication VARCHAR(50),
    Confidentiality_Impact VARCHAR(50),
    Integrity_Impact VARCHAR(50),
    Availability_Impact VARCHAR(50), 
    Obtain_All_Privilege BOOLEAN,
    Obtain_User_Privilege BOOLEAN,
    Obtain_Other_Privilege BOOLEAN,
    User_Interaction_Required BOOLEAN
)
""")
print("Table created.")

# Clean up
cursor.close()
conn.close()



