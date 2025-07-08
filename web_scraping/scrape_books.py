import requests
from bs4 import BeautifulSoup
import pandas as pd
import time  # for respectful scraping

# Base URL
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

books_data = []

# Loop through pages 1 to 50
for page in range(1, 51):
    print(f"\n--- Scraping Page {page} ---")
    url = BASE_URL.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        stock = book.find("p", class_="instock availability").text.strip()

        # Convert price to float (remove pound symbol)
        price_float = float(price.replace("£", ""))

        # Append the data to list
        books_data.append({
            "Title": title,
            "Price (GBP)": price_float,
            "Stock": stock
        })

        print(f"Title: {title}")
        print(f"Price: £{price_float}")
        print(f"Stock: {stock}\n")

    time.sleep(1)  # polite scraping delay

# Save to CSV
df = pd.DataFrame(books_data)
df.to_csv("filtered_books.csv", index=False)
print(f"\n✅ Saved {len(df)} books to filtered_books.csv")
