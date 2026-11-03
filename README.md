# Book Price Tracker

A full-stack Python project that scrapes book data from a practice site, stores it in a database, tracks price changes, and shows everything on a searchable web page.

## Features
- Scrapes all 1,000 books (title, price, rating, stock) across 50 pages
- Error handling for failed requests and a delay between requests
- Saves data in SQLite, with no duplicates on re-runs
- Logs every price change in a `price_history` table
- Flask web page with search by title and sorting by title, price and rating

## Tech Stack
Python, BeautifulSoup, Requests, SQLite, Flask, HTML/CSS (Jinja2 templates)

## How to Run
```
git clone https://github.com/Joshini04/price-tracker.git
cd price-tracker
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python database.py
python app.py
```
Then open http://127.0.0.1:5000

## Project Structure
- `scraper.py` : scrapes the website
- `database.py` : creates tables, saves books, detects price changes
- `app.py` : Flask web server
- `templates/index.html` : the web page

## Data Source
[books.toscrape.com](https://books.toscrape.com/), a site built for practising web scraping.