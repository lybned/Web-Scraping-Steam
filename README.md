# Web-Scraping-Steam

A web-scraper that will capture the top 50 games on sale from Steam.

## How to run
1. install all the python depenencies in requirements.txt.
2. Create your own .env file. The file should contain host, user, password, port and database.
3. Run database.py to create the targeted database and table.
4. Run data.py to pull data from Steam into your table.

After running data.py, a file "game_on_discount.csv" will be created to document the games pulled.