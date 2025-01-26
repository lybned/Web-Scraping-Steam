# Import necessary libraries

import requests
from bs4 import BeautifulSoup

# Import csv module
import csv

# Import regex
import re

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
cursor.execute(f"USE {database}")
url = "https://store.steampowered.com/search/?ignore_preferences=1&category1=998&specials=1&ndl=1"

# Send a GET request to the specified URL
response = requests.get(url)

# Get the content of the downloaded page and save in a variable
page_content = response.text


# Convert the file to a beautiful soup file
doc = BeautifulSoup(page_content, 'html.parser')

# Find all the games on the page
games = doc.find_all('div', {'class': 'responsive_search_name_combined'})

cursor.execute("DELETE FROM products")

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

        # Write to table
        cursor.execute("""
        INSERT INTO products (Name, Published_Date, Original_Price, Discount_Percentage, Discount_Price, Rating, Review_Rating, Reviews_Numbers)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, published_date, original_price, discount, discount_price, rating, review, review_num))
        connection.commit()
        print("Data inserted.")

# verify
cursor.execute("SELECT * FROM products")
rows = cursor.fetchall()
for row in rows:
    print(row)


# Clean up
cursor.close()
connection.close()