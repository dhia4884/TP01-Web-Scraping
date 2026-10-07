import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

url = "https://www.azquotes.com/top_quotes.html"

data = []

while url and len(data) < 1000:

    response = requests.get(url)

    if response.status_code != 200:
        print("Error:", response.status_code)
        break

    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("a", class_="title")

    for quote in quotes:
        text = quote.get_text(strip=True)

        if text and text not in data:
            data.append(text)

        if len(data) >= 1000:
            break

    print("Current page:", url)
    print("Quotes collected:", len(data))

    next_page = soup.find("li", class_="next")

    if next_page:
        next_link = next_page.find("a")

        if next_link:
            url = urljoin(url, next_link.get("href"))
        else:
            url = None
    else:
        url = None

df = pd.DataFrame(data[:1000], columns=["Quote"])

df.to_csv(
    "data/quotes.csv",
    index=False,
    encoding="utf-8-sig"
)

print("--------------------------------")
print("CSV file created successfully.")
print("Number of rows:", len(df))