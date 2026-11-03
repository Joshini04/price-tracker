# We'll have two tables (think of a table as an Excel sheet):

# books: one row per book (title, price, rating, stock)
# price_history: a log row every time a book's price changes

import sqlite3
from scraper import scrape_all #reuses the function from your scraper.py. 
#This is why we wrote if __name__ == "__main__": there, so importing doesn't trigger the printing

DB_NAME = "books.db"  # the database file that will be created


def create_tables():
    conn = sqlite3.connect(DB_NAME)  # opens books.db (creates it if missing)
    cursor = conn.cursor()  # the cursor is what runs SQL commands

    # CHANGED: title is no longer UNIQUE (two different books can share a title)
    # CHANGED: new url column, and url is UNIQUE because every book's link is different
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            price REAL,
            rating INTEGER,
            in_stock INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            old_price REAL,
            new_price REAL,
            changed_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()  # saves the changes
    conn.close()  # closes the file


def save_books(books):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    new_count = 0  # counts how many brand new books we add
    changed_count = 0  # counts how many books had a price change

    for book in books:
        # CHANGED: look for this book in the database by its url (not its title)
        # because titles can repeat but urls never do
        cursor.execute(
            "SELECT id, price FROM books WHERE url = ?",
            (book["url"],),
        )
        row = cursor.fetchone()  # the matching row, or None if not found

        if row is None:
            # book is not in the database yet, so add it
            # CHANGED: now also saves the url (5 columns, 5 question marks, 5 values)
            cursor.execute(
                "INSERT INTO books (title, url, price, rating, in_stock) VALUES (?, ?, ?, ?, ?)",
                (book["title"], book["url"], book["price"], book["rating"], int(book["in_stock"])),
            )
            new_count += 1
        else:
            book_id, old_price = row  # unpacks the row into two variables
            if old_price != book["price"]:
                # price changed, so log the change and update the book
                cursor.execute(
                    "INSERT INTO price_history (book_id, old_price, new_price) VALUES (?, ?, ?)",
                    (book_id, old_price, book["price"]),
                )
                cursor.execute(
                    "UPDATE books SET price = ? WHERE id = ?",
                    (book["price"], book_id),
                )
                changed_count += 1

    conn.commit()  # saves everything we did in the loop
    conn.close()
    return new_count, changed_count


if __name__ == "__main__":
    create_tables()  # makes the tables if they don't exist
    books = scrape_all()  # scrapes all 50 pages
    new_count, changed_count = save_books(books)  # saves them into the database
    print(f"\nNew books added: {new_count}")
    print(f"Prices changed: {changed_count}")