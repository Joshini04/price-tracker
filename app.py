from flask import Flask, render_template, request  # Flask builds the website
import sqlite3

app = Flask(__name__)  # creates the web app
DB_NAME = "books.db"  # the same database file database.py made


def get_books(search, sort):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # lets us read columns by name, like book["title"]
    cursor = conn.cursor()

    # maps what the dropdown sends to the matching SQL sorting text
    sort_options = {
        "title": "title ASC",
        "price_asc": "price ASC",
        "price_desc": "price DESC",
        "rating_desc": "rating DESC",
    }
    order_by = sort_options.get(sort, "title ASC")  # unknown value -> sort by title

    cursor.execute(
        f"SELECT title, price, rating, in_stock FROM books WHERE title LIKE ? ORDER BY {order_by}",
        (f"%{search}%",),  # % means "anything", so this matches the search text anywhere in the title
    )
    rows = cursor.fetchall()  # all matching books as a list
    conn.close()
    return rows


@app.route("/")  # runs when someone opens the home page
def index():
    search = request.args.get("search", "")  # reads ?search=... from the URL (empty if missing)
    sort = request.args.get("sort", "title")  # reads ?sort=... from the URL
    books = get_books(search, sort)
    return render_template("index.html", books=books, search=search, sort=sort)  # sends data to the HTML page


if __name__ == "__main__":
    app.run(debug=True)  # starts the website; debug=True shows errors in the browser