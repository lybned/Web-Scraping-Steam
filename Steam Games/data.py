# Import necessary libraries
import sqlalchemy
import requests
from bs4 import BeautifulSoup

# Import csv module
import csv

# Import regex
import re

import mysql.connector
from dotenv import load_dotenv
import os
from sqlalchemy import insert
from product import Product
# Load environment variables from .env file

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def clean_num(s):
    if s == None:
        return ""
    """Extracts only numbers and dots from a given string."""
    cleaned = re.sub(r'[^0-9.]', '', s)  # Remove all non-numeric and non-dot characters
    return cleaned


# Get the current date
current_date = datetime.now().date()

load_dotenv()
    
# Retrieve values from environment variables
host = os.getenv("MYSQL_HOST")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
port = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DATABASE")


url = "https://store.steampowered.com/search/?ignore_preferences=1&category1=998&specials=1&ndl=1"


engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

# Create a session to insert data
Session = sessionmaker(bind=engine)
session = Session()

# Send a GET request to the specified URL
response = requests.get(url)

# Get the content of the downloaded page and save in a variable
page_content = response.text


# Convert the file to a beautiful soup file
doc = BeautifulSoup(page_content, 'html.parser')

# Find all the games on the page
games = doc.find_all('div', {'class': 'responsive_search_name_combined'})

# Create the scraper component to save the result as a CSV file using the CSV module
with open('game_on_discount.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Published Date', 'Original Price', 'Discount Percentage', 'Discount Price', 'Rating','Review Rating' 'Reviews Numbers'])

    # Loop through each game and extract the relevant information
    for game in games:
        name = game.find('span', {'class': 'title'}).text.encode("ascii", errors="ignore").decode("ascii")
        published_date = game.find('div', {'class': 'col search_released responsive_secondrow'}).text.strip()

        discount_element = game.find('div', {'class': 'discount_block search_discount_block'})
        discount = discount_element.get('data-discount') if discount_element else None

        # Check if the element is present before accessing the text attribute
        original_price_elem = game.find('div', {'class': 'discount_original_price'})
        original_price = original_price_elem.text.strip() if original_price_elem else 'N/A'

        discount_price_elem = game.find('div', {'class': 'discount_final_price'})
        discount_price = discount_price_elem.text.strip() if discount_price_elem else 'N/A'

        # Extract review information using regular expressions
        review_summary = game.find('span', {'class': 'search_review_summary'})
        rating = ""
        review = ""
        if (review_summary):
            reviews_html = review_summary['data-tooltip-html'].split("<br>") if review_summary else 'N/A'
            if (len(reviews_html) > 1):
                rating = reviews_html[0]
                review = reviews_html[1]
        review_num = ""

        review_match = re.search(r"of the (.*?) user review", review)
        if review_match:
            review_num = review_match.group(1)

        # Write the extracted information to the CSV file
        # ['Name', 'Published Date', 'Original Price', 'Discount Price', 'Rating','Review Rating' 'Reviews Numbers']
        writer.writerow([name, published_date, original_price, discount,discount_price,rating,review, review_num])

        year = current_date.year
        month = current_date.month
        day = current_date.day

        # Convert to datetime object
        date_obj = datetime.strptime(published_date, "%d %b, %Y").date()
        day_diff = int((current_date - date_obj).days)
        # Write to table
        '''
        cursor.execute("""
        INSERT INTO products (Name, Published_Date, Original_Price, Discount_Percentage, Discount_Price, Rating, Review_Rating, Reviews_Numbers)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, published_date, original_price, discount, discount_price, rating, review, review_num))
        connection.commit()
        '''
        positive = int(clean_num(review[:5]))
        if (discount != None):
            new_game = Product(Name=name, Published_Date=published_date, Original_Price=clean_num(original_price), Discount_Percentage=clean_num(discount), Discount_Price=clean_num(discount_price), Rating=rating, Review_Rating=review, Reviews_Numbers=clean_num(review_num),
            Since_Release = day_diff,
            Positive = positive,
            Year = year, Month = month, Day = day)
            session.add(new_game)
            session.commit()

        print("Data inserted.")
print(current_date)
with open("log.txt", 'a+') as file:
    file.write(f"Pulled {len(games)} discounted games on {current_date}\n")

# input("Enter Anyting to Exit")

 