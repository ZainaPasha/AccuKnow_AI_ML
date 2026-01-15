import csv
import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    job_title TEXT,
    department TEXT,
    city TEXT,
    country TEXT
)
""")

with open("user_info.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        try:
            
            if not row["Id"] or not row["Username"]:
                continue

            cursor.execute("""
                INSERT INTO users (
                    id, username, first_name, last_name,
                    job_title, department, city, country
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                int(row["Id"]),
                row["Username"],
                row["Firstname"],
                row["Lastname"],
                row["Jobtitle"],
                row["Department"],
                row["City"],
                row["Country Or Region"]
            ))

        except Exception as e:
            print(f"Skipping row due to error: {e}")

conn.commit()
conn.close()

print("User data inserted successfully.")
