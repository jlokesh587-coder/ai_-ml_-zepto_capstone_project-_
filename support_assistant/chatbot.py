# 1. Install Streamlit and Localtunnel
!pip install -q streamlit
!npm install -g localtunnel -q

# 2. Write the Streamlit application code to app.py
with open("app.py", "w") as f:
    f.write("""
import sqlite3
import pandas as pd
import streamlit as st

def get_product_info(product_name):
    conn = sqlite3.connect("books_database.db")
    query = "SELECT * FROM Books WHERE title LIKE ?"
    df = pd.read_sql_query(
        query, conn, params=("%" + product_name + "%",)
    )
    conn.close()
    return df

st.title("E-commerce Product Support Chatbot")
user_input = st.text_input("Ask a question about our products:")

if user_input:
    product_df = get_product_info(user_input)
    if not product_df.empty:
        st.write("Here are the products found:")
        st.dataframe(product_df)
    else:
        st.write("Sorry, I couldn't find any products matching your query.")
""")

# 3. Retrieve your public IP address (needed to bypass localtunnel password screen)
print("Your Tunnel Password (IP Address) is:")
!curl ipv4.icanhazip.com

# 4. Start the Streamlit app in the background and expose it using localtunnel
import subprocess
subprocess.Popen(["streamlit", "run", "app.py", "--server.port", "8501"])

# Run localtunnel to expose port 8501
!npx localtunnel --port 8501
