import pandas as pd
import sqlite3
import re # Added for robust price parsing

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
    conn.commit()
    conn.close()
    print("Database schema created successfully.")

def populate_database(csv_file):
    create_database() # This now only creates the schema

    df = pd.read_csv(csv_file)

    conn = sqlite3.connect("books_database.db")
    cursor = conn.cursor()

    for _, row in df.iterrows():

        try:
            cursor.execute(
                "INSERT INTO Categories (category_name) VALUES (?)",
                (row["Category"],),
            )
        except sqlite3.IntegrityError:
            pass # Category already exists

        cursor.execute(
            "SELECT category_id FROM Categories WHERE category_name = ?",
            (row["Category"],),
        )
        category_id = cursor.fetchone()[0]

        # Use regex to remove all non-digit and non-dot characters for robust price parsing
        price_str = re.sub(r'[^\d.]', '', row["Price"])
        price = float(price_str)

        cursor.execute(
            """
            INSERT INTO Books (title, price, star_rating, availability, category_id)
            VALUES (?, ?, ?, ?, ?)
        """,
            (row["Title"], price, row["Star Rating"], row["Availability"], category_id),
        )

    conn.commit()
    conn.close()
    print("Database populated successfully!")


if __name__ == "__main__":
    populate_database("books_data.csv")
