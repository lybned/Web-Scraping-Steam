
import re
from dotenv import load_dotenv
import os
import mysql.connector



load_dotenv()
    
# Retrieve values from environment variables
host = os.getenv("MYSQL_HOST")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
port = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DATABASE")

# Database connection
# Connect to MySQL without specifying a database
conn = mysql.connector.connect(user=user, password=password, host=host, port=port)
cursor = conn.cursor()

# Use the specified database
cursor.execute(f"USE {database}")

cursor = conn.cursor()
# Fetch all data
cursor.execute("SELECT id, Reviews_Numbers FROM products")  # Select only necessary columns
rows = cursor.fetchall()

# Process and update the review column
for row in rows:
    print(row)
    clean_review = re.sub(r'[^0-9.]', '', str(row[1]))
    
    # Update the database
    cursor.execute(
        "UPDATE products SET Reviews_Numbers = %s WHERE id = %s",
        (clean_review, row[0])
    )

# Commit changes
conn.commit()

cursor.close()
conn.close()
    
