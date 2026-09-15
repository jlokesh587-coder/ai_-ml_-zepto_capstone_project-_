from database import create_database
import pandas as pd
import sqlite3


def populate_database(csv_file):
    create_database()

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
            pass

        cursor.execute(
            "SELECT category_id FROM Categories WHERE category_name = ?",
            (row["Category"],),
        )
        category_id = cursor.fetchone()[0]

        price = float(row["Price"].replace("£", ""))

        cursor.execute(
            """
            INSERT INTO Books (title, price, rating, availability, category_id)
            VALUES (?, ?, ?, ?, ?)
        """,
            (row["Title"], price, row["Star Rating"], row["Availability"], category_id),
        )

    conn.commit()
    conn.close()
    print("Database populated successfully!")


if __name__ == "__main__":
    populate_database("books_data.csv")
