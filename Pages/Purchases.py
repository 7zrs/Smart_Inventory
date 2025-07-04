import streamlit as st
import pandas as pd
import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api/purchases/"
PRODUCTS_URL = "http://127.0.0.1:8000/api/products/"

st.sidebar.title("🏢 Smart Inventory")
st.sidebar.divider()
st.sidebar.page_link("streamlit_app.py", label="🏠 Home")
st.sidebar.page_link("pages/Inventory.py", label="📦 Inventory")
st.sidebar.page_link("pages/Purchases.py", label="🛒 Purchases")
st.sidebar.page_link("pages/Sales.py", label="💰 Sales")
st.sidebar.page_link("pages/AI_Assistant.py", label="🤖 AI Assistant")

# Initialize session state
if 'show_add_success' not in st.session_state:
    st.session_state.show_add_success = False
if 'show_add_form' not in st.session_state:
    st.session_state.show_add_form = False
if 'show_edit_form' not in st.session_state:
    st.session_state.show_edit_form = False
if 'show_delete_confirm' not in st.session_state:
    st.session_state.show_delete_confirm = False
if 'selected_purchase_id' not in st.session_state:
    st.session_state.selected_purchase_id = None
if 'show_update_success' not in st.session_state:
    st.session_state.show_update_success = False
if 'show_delete_success' not in st.session_state:
    st.session_state.show_delete_success = False
if 'products' not in st.session_state:
    st.session_state.products = {}

def fetch_purchases():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            return response.json()
        st.error(f"Failed to fetch purchases: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        st.error(f"Failed to connect to the API: {e}")
        return None

def fetch_products():
    try:
        response = requests.get(PRODUCTS_URL)
        if response.status_code == 200:
            return response.json()
        st.error(f"Failed to fetch products: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        st.error(f"Failed to connect to the API: {e}")
        return None

def create_purchase(purchase_data):
    try:
        response = requests.post(BASE_URL, json=purchase_data)
        if response.status_code == 201:
            return True
        st.error(f"Failed to create purchase: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        st.error(f"API connection failed: {e}")
        return False

def update_purchase(purchase_id, purchase_data):
    try:
        response = requests.put(f"{BASE_URL}{purchase_id}/", json=purchase_data)
        if response.status_code == 200:
            return True
        st.error(f"Failed to update purchase: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        st.error(f"API connection failed: {e}")
        return False

def delete_purchase(purchase_id):
    try:
        response = requests.delete(f"{BASE_URL}{purchase_id}/")
        if response.status_code == 204:
            return True
        st.error(f"Failed to delete purchase: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        st.error(f"API connection failed: {e}")
        return False

# Load products data
products_data = fetch_products()
if products_data:
    st.session_state.products = {product['id']: product['name'] for product in products_data}

# Load and prepare purchases data
purchases_data = fetch_purchases()
df = pd.DataFrame()

if purchases_data:
    df = pd.DataFrame(purchases_data)
    # Replace product IDs with names
    df['product'] = df['product'].map(st.session_state.products)
    column_mapping = {
        'date': 'Date',
        'supplier': 'Supplier',
        'product': 'Product',
        'amount': 'Amount',
        'notes': 'Notes',
        'id': 'ID'
    }
    df = df.rename(columns=column_mapping)
else:
    df = pd.DataFrame(columns=["ID", "Date", "Supplier", "Product", "Amount", "Notes"])

# UI Components
st.title("🛒 Purchases")

st.markdown("""
<style>
    .stDataFrame > div:first-child {
        max-height: 210px !important;
        overflow-y: auto !important;
    }
    .stDataFrame thead th {
        position: sticky !important;
        top: 0 !important;
        background-color: white !important;
        z-index: 100 !important;
    }
    .stSelectbox > label {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Sort by date in descending order
if not df.empty:
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date', ascending=False)
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

st.dataframe(
    df[['Date', 'Supplier', 'Product', 'Amount', 'Notes']],
    use_container_width=True,
    hide_index=True,
    height=min(210, 35 * (len(df) + 1))
)

# Success Messages
if st.session_state.show_add_success:
    st.success("Purchase Added Successfully!")
    st.session_state.show_add_success = False

if st.session_state.show_update_success:
    st.success("Purchase Updated Successfully!")
    st.session_state.show_update_success = False

if st.session_state.show_delete_success:
    st.success("Purchase Deleted Successfully!")
    st.session_state.show_delete_success = False

# Action Section
st.divider()
st.write("#### ➕✏️🗑️ Actions:")
st.write("")

col_a, col_b = st.columns([2,5])

# Add Purchase Form
with col_a:
    if st.button("➕ Add New Purchase"):
        st.session_state.show_add_form = True
        st.session_state.show_edit_form = False
        st.session_state.show_delete_confirm = False
        st.rerun()

if st.session_state.show_add_form:
    with st.form("add_purchase_form"):
        st.subheader("Add New Purchase Details")
        date = st.date_input("Date*", value=datetime.now())
        supplier = st.text_input("Supplier", placeholder="Optional supplier name")
        
        # Create product selection dropdown
        product_options = {product['id']: product['name'] for product in products_data} if products_data else {}
        selected_product_id = st.selectbox(
            "Product*",
            options=list(product_options.keys()),
            format_func=lambda x: product_options[x]
        )
        
        amount = st.number_input("Amount*", min_value=1, value=1)
        notes = st.text_area("Notes", placeholder="Optional notes about the purchase")

        col1, col2 = st.columns(2)
        submitted = col1.form_submit_button("✅ Save Purchase")
        cancel = col2.form_submit_button("❌ Cancel")

        if submitted:
            new_purchase = {
                'date': str(date),
                'supplier': supplier,
                'product': selected_product_id,
                'amount': amount,
                'notes': notes
            }

            if create_purchase(new_purchase):
                st.session_state.show_add_success = True
                st.session_state.show_add_form = False
                st.rerun()

        if cancel:
            st.session_state.show_add_form = False
            st.rerun()

# Edit/Delete Purchase Section
with col_b:
    if not df.empty:    
        purchase_options = ["Select a purchase to edit or delete"] + [
            f"{row['Date']} - {row['Supplier']} - {row['Product']} ({row['Amount']})" 
            for _, row in df.iterrows()
        ]
        
        selected_purchase = st.selectbox(
            "hidden",
            options=purchase_options,
            key="purchase_selection",
        )

        selected_purchase_data = None
        if selected_purchase != "Select a purchase to edit or delete":
            parts = selected_purchase.split(" - ")
            selected_date = parts[0]
            selected_supplier = parts[1]
            selected_product = parts[2].split(" (")[0]
            selected_amount = parts[2].split(" (")[1].rstrip(")")
            
            matching_purchases = df[
                (df['Date'] == selected_date) & 
                (df['Supplier'] == selected_supplier) &
                (df['Product'] == selected_product) &
                (df['Amount'].astype(str) == selected_amount)
            ]
            
            if not matching_purchases.empty:
                selected_purchase_data = matching_purchases.iloc[0]
                st.session_state.selected_purchase_id = selected_purchase_data['ID']

        if selected_purchase_data is not None:
            st.write("")
            col_edit, col_delete = st.columns(2)

            if col_edit.button(f"✏️ Edit Purchase"):
                st.session_state.show_edit_form = True
                st.session_state.show_delete_confirm = False
                st.session_state.show_add_form = False
                st.rerun()

            if col_delete.button(f"🗑️ Delete Purchase"):
                st.session_state.show_delete_confirm = True
                st.session_state.show_edit_form = False
                st.session_state.show_add_form = False
                st.rerun()

    # Edit Purchase Form
    if st.session_state.show_edit_form and selected_purchase_data is not None:
        st.write("---")
        with st.form("edit_purchase_form"):
            st.subheader(f"Edit Purchase: {selected_purchase_data['Product']}")
            
            # Convert date string back to date object
            edit_date = st.date_input(
                "Date*", 
                value=datetime.strptime(selected_purchase_data['Date'], '%Y-%m-%d')
            )
            edit_supplier = st.text_input(
                "Supplier", 
                value=selected_purchase_data['Supplier']
            )
            
            # Product selection for edit
            current_product_id = [
                pid for pid, name in st.session_state.products.items() 
                if name == selected_purchase_data['Product']
            ][0]
            
            edit_product_id = st.selectbox(
                "Product*",
                options=list(st.session_state.products.keys()),
                index=list(st.session_state.products.keys()).index(current_product_id),
                format_func=lambda x: st.session_state.products[x]
            )
            
            edit_amount = st.number_input(
                "Amount*", 
                min_value=1, 
                value=int(selected_purchase_data['Amount'])
            )
            edit_notes = st.text_area(
                "Notes", 
                value=selected_purchase_data['Notes']
            )

            col_edit_submit, col_edit_cancel = st.columns(2)
            edit_submitted = col_edit_submit.form_submit_button("💾 Save Changes")
            edit_cancel = col_edit_cancel.form_submit_button("❌ Cancel Edit")

            if edit_submitted:
                updated_purchase = {
                    'date': str(edit_date),
                    'supplier': edit_supplier,
                    'product': edit_product_id,
                    'amount': edit_amount,
                    'notes': edit_notes
                }
                
                if update_purchase(st.session_state.selected_purchase_id, updated_purchase):
                    st.session_state.show_update_success = True
                    st.session_state.show_edit_form = False
                    st.session_state.selected_purchase_id = None
                    st.rerun()

            if edit_cancel:
                st.session_state.show_edit_form = False
                st.session_state.selected_purchase_id = None
                st.rerun()

    # Delete Confirmation
    if st.session_state.show_delete_confirm and selected_purchase_data is not None:
        st.warning(f"Are you sure you want to delete the purchase of **{selected_purchase_data['Amount']} {selected_purchase_data['Product']}** on **{selected_purchase_data['Date']}**? This action cannot be undone.")
        col_del_confirm, col_del_cancel = st.columns(2)

        if col_del_confirm.button("🗑️ Yes, Delete Purchase"):
            if delete_purchase(st.session_state.selected_purchase_id):
                st.session_state.show_delete_success = True
                st.session_state.show_delete_confirm = False
                st.session_state.selected_purchase_id = None
                st.rerun()
        if col_del_cancel.button("❌ Cancel Deletion"):
            st.session_state.show_delete_confirm = False
            st.session_state.selected_purchase_id = None
            st.rerun()