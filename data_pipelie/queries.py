import pandas as pd
import sqlite3
import re # Import the re module for regular expressions

def create_database():
    conn = sqlite3.connect("books_database.db")
    cursor = conn.cursor()

    # Drop tables if they exist (for clean rerun)
    cursor.execute("DROP TABLE IF EXISTS Books")
    cursor.execute("DROP TABLE IF EXISTS Categories")

    # Create Categories table
    cursor.execute("""
        CREATE TABLE Categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE
        )
    """)

    # Create Books table
    cursor.execute("""
        CREATE TABLE Books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            star_rating TEXT,
            availability TEXT,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES Categories (category_id)
        )
    """)

    # Load data from books_data.csv
    try:
        df = pd.read_csv("books_data.csv")
    except FileNotFoundError:
        print("Error: books_data.csv not found. Please run the scraping notebook first.")
        conn.close()
        return

    # Populate Categories table
    unique_categories = df["Category"].unique()
    for category in unique_categories:
        cursor.execute("INSERT INTO Categories (category_name) VALUES (?)", (category,))
    conn.commit()

    # Get category_id mapping
    category_map = {}
    cursor.execute("SELECT category_id, category_name FROM Categories")
    for row in cursor.fetchall():
        category_map[row[1]] = row[0]

    # Populate Books table
    for index, row in df.iterrows():
        title = row["Title"]
        # Price in CSV is like "£51.77", need to convert to float
        # Use regex to remove all non-digit and non-dot characters
        price_str = re.sub(r'[^\d.]', '', row["Price"])
        price = float(price_str)
        star_rating = row["Star Rating"]
        availability = row["Availability"]
        category_id = category_map.get(row["Category"])

        cursor.execute(
            """
            INSERT INTO Books (title, price, star_rating, availability, category_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, price, star_rating, availability, category_id),
        )
    conn.commit()
    conn.close()
    print("Database 'books_database.db' created and populated successfully.")


def run_queries():
    conn = sqlite3.connect("books_database.db")

    print("Query 1: All categories")
    categories_df = pd.read_sql("SELECT * FROM Categories", conn)
    print(categories_df)

    print("\nQuery 2: Books under £30")
    cheap_books_df = pd.read_sql("SELECT * FROM Books WHERE price < 30", conn)
    print(cheap_books_df)

    print("\nQuery 3: Books in 'Science Fiction' category")
    sf_books_df = pd.read_sql(
        """
        SELECT B.title, B.price
        FROM Books B
        JOIN Categories C ON B.category_id = C.category_id
        WHERE C.category_name = 'Science Fiction'
    """,
        conn,
    )
    print(sf_books_df)

    conn.close()
    print("\nQueries executed successfully!")


if __name__ == "__main__":
    create_database()
    run_queries()
