import streamlit as st
import sqlite3
import numpy as np
import pandas as pd
conn = sqlite3.connect('cafe.db')
c = conn.cursor()
def fetch_all_items_as_dataframe():
    c.execute("SELECT * FROM cafe_items")
    rows = c.fetchall()
    df = pd.DataFrame(rows, columns=['id', 'name', 'price', 'description'])
    return df

c.execute('''CREATE TABLE IF NOT EXISTS cafe_items (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             price REAL NOT NULL,
             description TEXT
             )''')
conn.commit()

def fetch_all_items():
    c.execute("SELECT * FROM cafe_items")
    rows = c.fetchall()
    return rows
def item_name_exists(name):
    c.execute("SELECT COUNT(*) FROM cafe_items WHERE name = ?", (name,))
    count = c.fetchone()[0]
    return count > 0
def add_item(name, price, description):
    if not item_name_exists(name):
        c.execute("INSERT INTO cafe_items (name, price, description) VALUES (?, ?, ?)", (name, price, description))
        conn.commit()
        st.success("Item added successfully!")
    else:
        st.error("Item with that name already exists. Please choose a unique name.")


def update_item(id, name, price, description):
    c.execute("UPDATE cafe_items SET name = ?, price = ?, description = ? WHERE id = ?", (name, price, description, id))
    conn.commit()
    st.success("Item updated successfully!")

def delete_item_by_name(name):
    if item_name_exists(name):
        c.execute("DELETE FROM cafe_items WHERE name = ?", (name,))
        conn.commit()
        st.success("Item deleted successfully!")
    else:
        st.error("Item with that name does not exist.")

st.title("Cafe Menu Management 🤎 ☕ 🧋")

selected_operation = st.sidebar.selectbox("CRUD Operation", ["Create", "Read", "Update", "Delete"])

if selected_operation == "Create":
    st.subheader("Add New Item")
    new_item_name = st.text_input("Item Name")
    new_item_price = st.number_input("Price (₹)", min_value=0.0)
    new_item_description = st.text_area("Description (Optional)")
    if st.button("Add Item"):
        add_item(new_item_name, new_item_price, new_item_description)

if selected_operation == "Read":
    st.subheader("Current Menu Items")
    items_df = fetch_all_items_as_dataframe()
    if not items_df.empty:
        st.dataframe(items_df, width=800, height=400)
    else:
        st.info("No items found in the menu.")

if selected_operation == "Update":
    items = fetch_all_items()
    if items:
        selected_item_id = st.sidebar.selectbox("Select Item to Update", [item[0] for item in items])
        if selected_item_id:
            c.execute("SELECT * FROM cafe_items WHERE id = ?", (selected_item_id,))
            item_to_update = c.fetchone()
            st.subheader("Update Item")
            updated_name = st.text_input("Item Name", item_to_update[1])
            updated_price = st.number_input("Price (₹)", min_value=0.0, value=item_to_update[2])
            updated_description = st.text_area("Description", item_to_update[3])
            if st.button("Update Item"):
                update_item(selected_item_id, updated_name, updated_price, updated_description)

if selected_operation == "Delete":
    st.subheader("Delete Item by Name")
    item_to_delete_name = st.text_input("Enter Item Name")
    if st.button("Delete Item", key="delete"):  # Added key to prevent accidental deletion
        delete_item_by_name(item_to_delete_name)

conn.close()
