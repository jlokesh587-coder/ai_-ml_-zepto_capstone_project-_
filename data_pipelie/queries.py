from database import create_database
import pandas as pd
import sqlite3


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
    run_queries()
