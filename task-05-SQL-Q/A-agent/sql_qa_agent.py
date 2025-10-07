import os
import random
import sqlite3
from datetime import datetime, timedelta
import gradio as gr
from dotenv import load_dotenv
import re

# LangChain + Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import SQLDatabase

# Gemini SDK
import google.generativeai as genai

# --------------------------
# 1️⃣ Load API Key
# --------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("⚠️ Please set GEMINI_API_KEY in your .env file")

# --------------------------
# 2️⃣ Configure Gemini & Select Model
# --------------------------
genai.configure(api_key=api_key)
models_list = list(genai.list_models())
model_name = next((m.name for m in models_list if "gemini-pro" in m.name), models_list[0].name)
print(f"✅ Using model: {model_name}")

# --------------------------
# 3️⃣ Create SQLite Database
# --------------------------
db_file = "ecommerce.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    email TEXT,
    region TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    rating REAL
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    order_date TEXT,
    total_price REAL,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
);
""")

# Seed customers
regions = ['North', 'South', 'East', 'West']
customers_data = [
    (i, f'Customer{i}', random.randint(18, 60), f'customer{i}@email.com', random.choice(regions))
    for i in range(1, 51)
]
cursor.executemany('INSERT OR IGNORE INTO customers VALUES (?, ?, ?, ?, ?)', customers_data)

# Seed products
products_data = [
    (1, 'Laptop', 'Electronics', 800.0, 4.5),
    (2, 'Headphones', 'Electronics', 50.0, 4.2),
    (3, 'Coffee Maker', 'Home Appliances', 120.0, 4.0),
    (4, 'Office Chair', 'Furniture', 200.0, 4.3),
    (5, 'Sneakers', 'Footwear', 90.0, 4.6),
    (6, 'Smartphone', 'Electronics', 600.0, 4.4),
    (7, 'Backpack', 'Accessories', 40.0, 4.1),
    (8, 'Watch', 'Accessories', 150.0, 4.2),
    (9, 'Table Lamp', 'Home Appliances', 60.0, 4.0),
    (10, 'Jeans', 'Clothing', 70.0, 4.3),
    (11, 'T-Shirt', 'Clothing', 25.0, 4.1),
    (12, 'Blender', 'Home Appliances', 80.0, 4.2),
    (13, 'Gaming Console', 'Electronics', 400.0, 4.7),
    (14, 'Microwave', 'Home Appliances', 150.0, 4.3),
    (15, 'Sofa', 'Furniture', 500.0, 4.4),
    (16, 'Sandals', 'Footwear', 45.0, 4.0),
    (17, 'Jacket', 'Clothing', 120.0, 4.5),
    (18, 'Camera', 'Electronics', 350.0, 4.6),
    (19, 'Desk', 'Furniture', 220.0, 4.2),
    (20, 'Headset', 'Electronics', 70.0, 4.3)
]
cursor.executemany('INSERT OR IGNORE INTO products VALUES (?, ?, ?, ?, ?)', products_data)

# Seed orders
orders_data = []
start_date = datetime(2025, 1, 1)
for order_id in range(1, 151):
    customer_id = random.randint(1, 50)
    product_id = random.randint(1, 20)
    quantity = random.randint(1, 3)
    order_date = start_date + timedelta(days=random.randint(0, 60))
    price = next(p[3] for p in products_data if p[0] == product_id)
    total_price = price * quantity
    orders_data.append((order_id, customer_id, product_id, quantity, order_date.strftime('%Y-%m-%d'), total_price))
cursor.executemany('INSERT OR IGNORE INTO orders VALUES (?, ?, ?, ?, ?, ?)', orders_data)

conn.commit()
conn.close()
print("✅ Database 'ecommerce.db' created successfully!")

# --------------------------
# 4️⃣ LangChain SQL QA Chain
# --------------------------
llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
db = SQLDatabase.from_uri(f"sqlite:///{db_file}")

prompt = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template="""
You are a helpful data analyst. Given the table schema and a user question, write a safe SQL query to answer it.

Schema:
{table_info}

Question:
{input}

Only use columns that exist. Limit results to {top_k} rows if applicable.
""",
)

sql_chain = SQLDatabaseChain.from_llm(
    llm=llm,
    db=db,
    prompt=prompt,
    return_intermediate_steps=True,
    verbose=True,
)

# --------------------------
# 5️⃣ Gradio Chat UI
# --------------------------
def strip_markdown_sql(sql_text):
    return re.sub(r"```sql|```", "", sql_text).strip()

with gr.Blocks(title="🛒 E-Commerce SQL QA Agent") as demo:
    gr.Markdown("## 🛒 E-Commerce SQL QA Agent\nAsk questions about customers, products, and orders.")
    chatbot = gr.Chatbot(height=400, type="messages")
    msg = gr.Textbox(placeholder="Ask something like 'Top 5 products by revenue'")
    clear = gr.Button("Clear")

    def answer_query(user, history):
        try:
            result = sql_chain.invoke({"query": user})
            raw_sql = result["intermediate_steps"]["sql_cmd"]
            clean_sql = strip_markdown_sql(raw_sql)
            db_result = db.run(clean_sql)
            answer = f"{result['result']}\n\n📊 Query Result:\n{db_result}"
        except Exception as e:
            answer = f"⚠️ SQL execution failed: {str(e)}"
            clean_sql = "Query could not be executed."

        full_reply = f"{answer}\n\n🧠 SQL Used:\n```sql\n{clean_sql}\n```"
        return history + [
            {"role": "user", "content": user},
            {"role": "assistant", "content": full_reply}
        ], ""

    msg.submit(answer_query, [msg, chatbot], [chatbot, msg])
    clear.click(lambda: [], None, chatbot, queue=False)

# --------------------------
# 6️⃣ Launch
# --------------------------
if __name__ == "__main__":
    demo.launch()
