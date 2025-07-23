import sqlite3
import pandas as pd
import os

DB_PATH = "ecommerce.db"

def load_csv_to_sqlite():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if tables already exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='total_sales_df';")
    if cursor.fetchone():
        print("✅ Tables already exist. Skipping reload.")
        conn.close()
        return

    print("📦 Loading CSVs into SQLite...")

    eligibility_df = pd.read_csv("eligibility.csv")
    ad_sales_df = pd.read_csv("ad_sales.csv")
    total_sales_df = pd.read_csv("total_sales.csv")

    eligibility_df.to_sql("eligibility_df", conn, if_exists="replace", index=False)
    ad_sales_df.to_sql("ad_sales_df", conn, if_exists="replace", index=False)
    total_sales_df.to_sql("total_sales_df", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()
    print("✅ CSV data loaded into SQLite.")

if __name__ == "__main__":
    load_csv_to_sqlite()
