from bs4 import BeautifulSoup
import requests
import pandas as pd


def scrape_books():
    base_url = "http://books.toscrape.com/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    categories = (
        soup.find("ul", class_="nav-list").find("li").find("ul").find_all("a")
    )

    all_books = []

    for category in categories[:3]:
        cat_url = base_url + category["href"]
        cat_name = category.text.strip()
        print(f"Scraping category: {cat_name}")

        cat_response = requests.get(cat_url)
        cat_soup = BeautifulSoup(cat_response.text, "html.parser")
        books = cat_soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.find("h3").find("a")["title"]
            price = book.find("p", class_="price_color").text.strip()
            rating_classes = book.find("p", class_="star-rating")["class"]
            rating = rating_classes[1]
            availability = (
                book.find("p", class_="instock availability").text.strip()
            )

            all_books.append(
                {
                    "Title": title,
                    "Price": price,
                    "Star Rating": rating,
                    "Availability": availability,
                    "Category": cat_name,
                }
            )

    df = pd.DataFrame(all_books)
    df.to_csv("books_data.csv", index=False)
    print("Scraping completed!")


if __name__ == "__main__":
    scrape_books()
