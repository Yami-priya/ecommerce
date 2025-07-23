#yamini(21MIS0085)
from flask import Flask, request, jsonify
import sqlite3, os, re
import ollama
from db_loader import load_csv_to_sqlite

app = Flask(__name__)
DB_PATH = "ecommerce.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_db_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    schema = ""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for (table,) in cursor.fetchall():
        schema += f"\nTable: {table}\n"
        cursor.execute(f"PRAGMA table_info({table});")
        for col in cursor.fetchall():
            schema += f"  - {col[1]} ({col[2]})\n"
    conn.close()
    return schema

def map_question_to_query(question):
    question = question.lower()
    if "total sales" in question:
        return "SELECT SUM(total_sales) AS total_sales FROM total_sales_df;"
    elif "total units ordered" in question:
        return "SELECT SUM(total_units_ordered) AS total_units FROM total_sales_df;"
    elif "top selling item" in question:
        return """
        SELECT item_id, SUM(total_units_ordered) AS units_sold
        FROM total_sales_df
        GROUP BY item_id
        ORDER BY units_sold DESC
        LIMIT 1;"""
    elif "ad spend" in question:
        return "SELECT SUM(ad_spend) AS total_ad_spend FROM ad_sales_df;"
    elif "eligibility status" in question:
        return "SELECT item_id, eligibility FROM eligibility_df;"
    elif "clicks" in question:
        return "SELECT SUM(clicks) AS total_clicks FROM ad_sales_df;"
    elif "roas" in question or "return on ad spend" in question:
        return """
        SELECT 
            CASE WHEN SUM(ad_spend) = 0 THEN 0 ELSE ROUND(SUM(ad_sales) / SUM(ad_spend), 2) END AS RoAS
        FROM ad_sales_df;"""
    elif "highest cpc" in question:
        return """
        SELECT item_id, ROUND(ad_spend * 1.0 / clicks, 2) AS CPC
        FROM ad_sales_df
        WHERE clicks > 0
        ORDER BY CPC DESC
        LIMIT 1;"""
    return None

def execute_sql(query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return columns, rows

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")

    query = map_question_to_query(question)

    if query is None:
        schema = get_db_schema()
        prompt = f"""
You are an expert SQLite assistant. Given the schema below, write ONLY a valid SQLite query for the user's question. No explanations.

Schema:
{schema}

User question: {question}
"""
        res = ollama.generate(model="tinyllama", prompt=prompt)
        raw_response = res['response'].strip()
        match = re.search(r"(?i)(select|with|insert|delete|update)[^;]*;", raw_response, re.DOTALL)
        query = match.group(0).strip() if match else raw_response

    try:
        columns, rows = execute_sql(query)
        results = [dict(zip(columns, row)) for row in rows]
        return jsonify({"question": question, "query": query, "results": results})
    except Exception as e:
        return jsonify({"error": str(e), "query": query})

if __name__ == "__main__":
    load_csv_to_sqlite()
    app.run(debug=True)
