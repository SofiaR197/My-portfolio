import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "http://books.toscrape.com/catalogue/page-{}.html"

all_books = []


for page in range(1, 51):
    url = base_url.format(page)
    response = requests.get(url)


    if response.status_code != 200:
        break

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        rating = book.p["class"][1]

        all_books.append({"Title": title, "Price": price, "Rating": rating})

df = pd.DataFrame(all_books)
df.to_csv("all_books.csv", index=False, encoding="utf-8")

print(f"✅ Scraped {len(all_books)} books and saved to all_books.csv")
