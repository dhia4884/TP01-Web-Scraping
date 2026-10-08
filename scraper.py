import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

url = "https://www.azquotes.com/top_quotes.html"

data = []

while url:

    response = requests.get(url)

    if response.status_code != 200:
        print("Error:", response.status_code)
        break

    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("a", class_="title")

    for quote in quotes:

        text = quote.get_text(strip=True)

        if not text:
            continue

        # الوصول إلى العنصر الأب الخاص بالـ Quote
        quote_box = quote.find_parent("div", class_="wrap-block")

        author = ""
        tags = ""

        if quote_box:

            # استخراج Author
            author_tag = quote_box.find("div", class_="author")

            if author_tag:
                author = author_tag.get_text(strip=True)

            # استخراج Tags
            tag_elements = quote_box.find_all("a", class_="tag")

            tags_list = []

            for tag in tag_elements:
                tag_text = tag.get_text(strip=True)

                if tag_text:
                    tags_list.append(tag_text)

            tags = ", ".join(tags_list)

        # التأكد من عدم وجود Quote مكرر
        if text not in [item["Quote"] for item in data]:

            data.append({
                "Quote": text,
                "Author": author,
                "Tags": tags
            })

    print("Current page:", url)
    print("Quotes collected:", len(data))

    # الانتقال إلى الصفحة التالية
    next_page = soup.find("li", class_="next")

    if next_page:

        next_link = next_page.find("a")

        if next_link:
            url = urljoin(url, next_link.get("href"))
        else:
            url = None

    else:
        url = None


# إنشاء DataFrame بجميع البيانات
df = pd.DataFrame(
    data,
    columns=["Quote", "Author", "Tags"]
)

# حفظ جميع البيانات في CSV
df.to_csv(
    "data/quotes.csv",
    index=False,
    encoding="utf-8-sig"
)

print("--------------------------------")
print("CSV file created successfully.")
print("Number of rows:", len(df))
print("Columns:", list(df.columns))