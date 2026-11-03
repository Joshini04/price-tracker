import time #used for the pause between pages
import requests #loads the library that downloads web pages
from bs4 import BeautifulSoup #loads the library that reads HTML.

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html" # the page we scrape
#The {} is an empty slot that gets filled with a page number, so one line can make all 50 URLs
TOTAL_PAGES = 50 # pages each with 20 books, so 1000 books total. The site has 50 pages of books.

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
# converts the website’s rating words into numbers. 
# The site stores ratings as words (like “Three”), and numbers are easier to sort later.

def scrape_page(url):
    response = requests.get(url, timeout=10) 
    #downloads the page. timeout=10 means give up after 10 seconds instead of hanging forever.
    response.raise_for_status()
    # If the website returns an error (404, 500),
    # this raises an error on purpose instead of quietly reading the error page as normal
    response.encoding = "utf-8"
    #tells Python how to read the text. Without it, the £ sign can show up as Â£.
    soup = BeautifulSoup(response.text, "html.parser")
    #turns the raw HTML into something we can search

    books = []
    #for card in ... goes through the boxes one at a time
    for card in soup.select("article.product_pod"): #finds every book box on the page
        #Each book is wrapped in an <article class="product_pod"> tag, and this returns all 20 of them.
        title = card.h3.a["title"]
        #gets the full title from the link inside the <h3> tag
        url = card.h3.a["href"]
        #reads the link of the book’s title. Each book’s link is different
        #so it works as an ID

        price_text = card.select_one("p.price_color").text
        #gets the price text
        price = float(price_text.replace("£", ""))
        #removes the pound sign, and
        # float(...) turns the text into a number so we can sort and compare prices.

        rating_word = card.select_one("p.star-rating")["class"][1] #gets the rating
        #The HTML looks like <p class="star-rating Three">, (the three here is an example)
        # so ["class"] gives ["star-rating", "Three"], and [1] picks the second item, "Three"
        rating = RATING_MAP[rating_word] #converts "Three" to 3

        in_stock = "In stock" in card.select_one("p.availability").text
        #gives True if the availability text contains “In stock”, otherwise False
        books.append({ 
            #saves this book as a dictionary (a labelled bundle of data) in our books list
            "title": title,
            "url": url, #This saves the link in each book’s dictionary so database.py can use it
            "price": price,
            "rating": rating,
            "in_stock": in_stock,
        })

    return books #hands the finished list back to whoever called the function

def scrape_all(total_pages=TOTAL_PAGES):  #A new function that scrapes every page by calling scrape_page for each one
    all_books = []    #An empty list that will collect all 1,000 books

    for page_number in range(1, total_pages + 1):  
        url = BASE_URL.format(page_number)  #Fills the {} slot with the current page number, so page 3 becomes .../page-3.html
        try:  #try the code below, and if something fails, don’t crash
            books = scrape_page(url)  #Scrapes this one page and stores its 20 books in books
            all_books.extend(books)  #Adds those 20 books into the big list, one by one
            print(f"Page {page_number}/{total_pages}: {len(books)} books") 
            #Shows progress, like Page 3/50: 20 books
        except requests.RequestException as error: 
            #If the download fails (no internet, timeout, bad status), jump here instead of crashing
            print(f"Page {page_number} failed: {error}")  

        time.sleep(0.5)  #Pauses half a second between pages

    return all_books  


if __name__ == "__main__":
    books = scrape_all()  # 
    print(f"\nTotal books collected: {len(books)}")  #