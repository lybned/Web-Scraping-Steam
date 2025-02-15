# Import necessary libraries
import sqlalchemy

import json
import mysql.connector
from dotenv import load_dotenv
import os
from sqlalchemy import insert
from vul_class import Vuls
# Load environment variables from .env file

from datetime import date
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get the current date
current_date = date.today()

load_dotenv()
    
# Retrieve values from environment variables
host = os.getenv("MYSQL_HOST")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
port = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DATABASE")


engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

# Set up the sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

current_date = date.today()
year = current_date.year
month = current_date.month
day = current_date.day

print(current_date)
# Query the 'users' table with filters for 'id' and 'name'
vuls = session.query(Vuls).all()
#games = session.query(Product).all()
# Print the results
if vuls:
    for item in vuls:
        print(f"{item.id}: {item.CVE_ID}, {item.Published_Date}, {item.Status} ..")