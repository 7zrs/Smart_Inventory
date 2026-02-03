import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from Pages.login import handle_logout

# Check if user is authenticated
if 'auth' not in st.session_state or not st.session_state.auth.get('authenticated', False):
    st.switch_page("pages/login.py")
    st.stop()

BASE_URL = "http://127.0.0.1:8000/api/purchases/"
PRODUCTS_URL = "http://127.0.0.1:8000/api/products/"

st.sidebar.title("🏢 Smart Inventory")
st.sidebar.divider()
st.sidebar.page_link("streamlit_app.py", label="🏠 Home")
st.sidebar.page_link("pages/Inventory.py", label="📦 Inventory")
st.sidebar.page_link("pages/Purchases.py", label="🛒 Purchases")
st.sidebar.page_link("pages/Sales.py", label="💰 Sales")
st.sidebar.page_link("pages/AI_Assistant.py", label="🤖 AI Assistant")
st.sidebar.divider()
if st.sidebar.button("🚪 Logout"):
    handle_logout()
    st.switch_page("pages/login.py")
if st.session_state.auth.get('is_admin', False):
    if st.sidebar.button("↩️ Admin Dashboard"):
        st.switch_page("pages/login.py")

# Initialize session state (page-specific keys to avoid conflicts)
if 'purch_show_add_success' not in st.session_state:
    st.session_state.purch_show_add_success = False
if 'purch_show_update_success' not in st.session_state:
    st.session_state.purch_show_update_success = False
if 'purch_show_delete_success' not in st.session_state:
    st.session_state.purch_show_delete_success = False
if 'purch_selected_id' not in st.session_state:
    st.session_state.purch_selected_id = None
if 'purch_show_edit_dialog' not in st.session_state:
    st.session_state.purch_show_edit_dialog = False
if 'purch_show_delete_dialog' not in st.session_state:
    st.session_state.purch_show_delete_dialog = False
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
            return True, None
        return False, f"Failed to create purchase: {response.status_code} - {response.text}"
    except Exception as e:
        return False, f"API connection failed: {e}"

def update_purchase(purchase_id, purchase_data):
    try:
        response = requests.put(f"{BASE_URL}{purchase_id}/", json=purchase_data)
        if response.status_code == 200:
            return True, None
        return False, f"Failed to update purchase: {response.status_code} - {response.text}"
    except Exception as e:
        return False, f"API connection failed: {e}"

def delete_purchase(purchase_id):
    try:
        response = requests.delete(f"{BASE_URL}{purchase_id}/")
        if response.status_code == 204:
            return True, None
        return False, f"Failed to delete purchase: {response.status_code} - {response.text}"
    except Exception as e:
        return False, f"API connection failed: {e}"


# Load products data first (needed for dialogs)
products_data = fetch_products()
if products_data:
    st.session_state.products = {product['id']: product['name'] for product in products_data}
    st.session_state.products_list = products_data


# Dialog for adding new purchase
@st.dialog("Add New Purchase")
def add_purchase_dialog():
    date = st.date_input("Date*", value=datetime.now())
    supplier = st.text_input("Supplier", placeholder="Optional supplier name")

    product_options = {p['id']: p['name'] for p in st.session_state.get('products_list', [])}
    if product_options:
        selected_product_id = st.selectbox(
            "Product*",
            options=list(product_options.keys()),
            format_func=lambda x: product_options[x]
        )
    else:
        st.warning("No products available. Please add products first.")
        selected_product_id = None

    amount = st.number_input("Amount*", min_value=1, value=1)
    notes = st.text_area("Notes", placeholder="Optional notes about the purchase")

    col1, col2 = st.columns(2)
    if col1.button("✅ Save Purchase", use_container_width=True):
        if selected_product_id:
            new_purchase = {
                'date': str(date),
                'supplier': supplier,
                'product': selected_product_id,
                'amount': amount,
                'notes': notes
            }
            success, error = create_purchase(new_purchase)
            if success:
                st.session_state.purch_show_add_success = True
                st.rerun()
            else:
                st.error(error)
        else:
            st.warning("Please select a product")

    if col2.button("❌ Cancel", use_container_width=True):
        st.rerun()


# Dialog for editing purchase
@st.dialog("Edit Purchase")
def edit_purchase_dialog(purchase_data, purchase_id):
    edit_date = st.date_input(
        "Date*",
        value=datetime.strptime(purchase_data['Date'], '%Y-%m-%d')
    )
    edit_supplier = st.text_input("Supplier", value=purchase_data['Supplier'] if purchase_data['Supplier'] else "")

    # Find current product ID
    current_product_id = None
    for pid, name in st.session_state.products.items():
        if name == purchase_data['Product']:
            current_product_id = pid
            break

    product_keys = list(st.session_state.products.keys())
    current_index = product_keys.index(current_product_id) if current_product_id in product_keys else 0

    edit_product_id = st.selectbox(
        "Product*",
        options=product_keys,
        index=current_index,
        format_func=lambda x: st.session_state.products[x]
    )

    edit_amount = st.number_input("Amount*", min_value=1, value=int(purchase_data['Amount']))
    edit_notes = st.text_area("Notes", value=purchase_data['Notes'] if purchase_data['Notes'] else "")

    col1, col2 = st.columns(2)
    if col1.button("💾 Save Changes", use_container_width=True):
        updated_purchase = {
            'date': str(edit_date),
            'supplier': edit_supplier,
            'product': edit_product_id,
            'amount': edit_amount,
            'notes': edit_notes
        }
        success, error = update_purchase(purchase_id, updated_purchase)
        if success:
            st.session_state.purch_show_update_success = True
            st.session_state.purch_show_edit_dialog = False
            st.session_state.purch_selected_id = None
            st.rerun()
        else:
            st.error(error)

    if col2.button("❌ Cancel", use_container_width=True):
        st.session_state.purch_show_edit_dialog = False
        st.session_state.purch_selected_id = None
        st.rerun()


# Dialog for delete confirmation
@st.dialog("Confirm Delete")
def delete_purchase_dialog(purchase_data, purchase_id):
    st.warning(f"Are you sure you want to delete the purchase of **{purchase_data['Amount']} {purchase_data['Product']}** on **{purchase_data['Date']}**?")
    st.caption("This action cannot be undone.")

    col1, col2 = st.columns(2)
    if col1.button("🗑️ Yes, Delete", use_container_width=True, type="primary"):
        success, error = delete_purchase(purchase_id)
        if success:
            st.session_state.purch_show_delete_success = True
            st.session_state.purch_show_delete_dialog = False
            st.session_state.purch_selected_id = None
            st.rerun()
        else:
            st.error(error)

    if col2.button("❌ Cancel", use_container_width=True):
        st.session_state.purch_show_delete_dialog = False
        st.session_state.purch_selected_id = None
        st.rerun()


# Load and prepare purchases data
purchases_data = fetch_purchases()
df = pd.DataFrame()

if purchases_data:
    df = pd.DataFrame(purchases_data)
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
if st.session_state.purch_show_add_success:
    st.success("Purchase Added Successfully!")
    st.session_state.purch_show_add_success = False

if st.session_state.purch_show_update_success:
    st.success("Purchase Updated Successfully!")
    st.session_state.purch_show_update_success = False

if st.session_state.purch_show_delete_success:
    st.success("Purchase Deleted Successfully!")
    st.session_state.purch_show_delete_success = False

# Action Section
st.divider()
st.write("#### ➕✏️🗑️ Actions:")
st.write("")

col_a, col_b = st.columns([2, 5])

# Add Purchase Button
with col_a:
    if st.button("➕ Add New Purchase"):
        add_purchase_dialog()

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
            label_visibility="collapsed"
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
                st.session_state.purch_selected_id = selected_purchase_data['ID']

        if selected_purchase_data is not None:
            st.write("")
            col_edit, col_delete = st.columns(2)

            with col_edit:
                if st.button("✏️ Edit Purchase"):
                    st.session_state.purch_show_edit_dialog = True

            with col_delete:
                if st.button("🗑️ Delete Purchase"):
                    st.session_state.purch_show_delete_dialog = True

# Show dialogs based on state
if st.session_state.purch_show_edit_dialog and st.session_state.purch_selected_id:
    matching = df[df['ID'] == st.session_state.purch_selected_id]
    if not matching.empty:
        purchase_data = matching.iloc[0]
        edit_purchase_dialog(purchase_data, st.session_state.purch_selected_id)

if st.session_state.purch_show_delete_dialog and st.session_state.purch_selected_id:
    matching = df[df['ID'] == st.session_state.purch_selected_id]
    if not matching.empty:
        purchase_data = matching.iloc[0]
        delete_purchase_dialog(purchase_data, st.session_state.purch_selected_id)
