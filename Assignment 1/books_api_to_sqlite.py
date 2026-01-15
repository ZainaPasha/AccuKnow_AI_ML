import requests
import sqlite3

# 1. Fetch data from Open Library API
url = "https://openlibrary.org/search.json?q=python"
response = requests.get(url)
data = response.json()

books = data["docs"][:10]  

# 2. Connect to SQLite
conn = sqlite3.connect("books.db")
cursor = conn.cursor()

# 3. Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    publish_year INTEGER
)
""")

# 4. Insert data
for book in books:
    title = book.get("title")
    author = book.get("author_name", ["Unknown"])[0]
    year = book.get("first_publish_year")

    cursor.execute(
        "INSERT INTO books (title, author, publish_year) VALUES (?, ?, ?)",
        (title, author, year)
    )

conn.commit()

# 5. Read & display data
cursor.execute("SELECT title, author, publish_year FROM books")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
