import streamlit as st
import requests

# API base URL
BASE_URL = "http://127.0.0.1:8000/api/products/"

# Function to fetch all products
def fetch_products():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return response.json()
    return []

# Function to create a new product
def create_product(product_data):
    response = requests.post(BASE_URL, json=product_data)
    return response.status_code == 201

# Function to update a product
def update_product(product_id, product_data):
    response = requests.put(f"{BASE_URL}{product_id}/", json=product_data)
    return response.status_code == 200

# Function to delete a product
def delete_product(product_id):
    response = requests.delete(f"{BASE_URL}{product_id}/")
    return response.status_code == 204

# Streamlit App
st.title("Inventory Management Dashboard")

# Sidebar for adding a new product
st.sidebar.header("Add New Product")
with st.sidebar.form("add_product_form"):
    name = st.text_input("Name")
    unit = st.text_input("Unit (e.g., pieces, kilograms)")
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Add Product")
    if submitted:
        product_data = {
            "name": name,
            "unit": unit,
            "notes": notes,
        }
        if create_product(product_data):
            st.sidebar.success("Product added successfully!")
        else:
            st.sidebar.error("Failed to add product.")

# Main area to display products
st.header("Product List")
products = fetch_products()

if products:
    for product in products:
        with st.expander(f"{product['name']} ({product['unit']})"):
            st.write(f"**Notes:** {product['notes']}")
            st.write(f"**Purchased Amount:** {product['purchased_amount']}")
            st.write(f"**Sold Amount:** {product['sold_amount']}")
            st.write(f"**Stock Level:** {product['stock_level']}")

            # Update and delete buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update", key=f"update_{product['id']}"):
                    st.session_state['update_product_id'] = product['id']
            with col2:
                if st.button("Delete", key=f"delete_{product['id']}"):
                    if delete_product(product['id']):
                        st.success("Product deleted successfully!")
                    else:
                        st.error("Failed to delete product.")
else:
    st.warning("No products found. Add a new product using the sidebar.")

# Update product form
if 'update_product_id' in st.session_state:
    st.header("Update Product")
    product_id = st.session_state['update_product_id']
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        with st.form("update_product_form"):
            name = st.text_input("Name", value=product['name'])
            unit = st.text_input("Unit (e.g., pieces, kilograms)", value=product['unit'])
            notes = st.text_area("Notes", value=product['notes'])
            submitted = st.form_submit_button("Update Product")
            if submitted:
                product_data = {
                    "name": name,
                    "unit": unit,
                    "notes": notes,
                }
                if update_product(product_id, product_data):
                    st.success("Product updated successfully!")
                    del st.session_state['update_product_id']
                else:
                    st.error("Failed to update product.")
    else:
        st.error("Product not found.")