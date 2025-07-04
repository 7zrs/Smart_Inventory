import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from Pages.login import handle_logout

# Check if user is authenticated 
if 'auth' not in st.session_state or not st.session_state.auth.get('authenticated', False):
    # Redirect to login page
    st.switch_page("pages/login.py")  
    st.stop()  # Stop execution of the rest of the page

BASE_URL = "http://127.0.0.1:8000/api/sales/"
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
# Admin-only 
if st.session_state.auth.get('is_admin', False):
    if st.sidebar.button("↩️ Admin Dashboard"):
        st.switch_page("pages/login.py")

# Initialize session state
if 'show_add_success' not in st.session_state:
    st.session_state.show_add_success = False
if 'show_add_form' not in st.session_state:
    st.session_state.show_add_form = False
if 'show_edit_form' not in st.session_state:
    st.session_state.show_edit_form = False
if 'show_delete_confirm' not in st.session_state:
    st.session_state.show_delete_confirm = False
if 'selected_sale_id' not in st.session_state:
    st.session_state.selected_sale_id = None
if 'show_update_success' not in st.session_state:
    st.session_state.show_update_success = False
if 'show_delete_success' not in st.session_state:
    st.session_state.show_delete_success = False
if 'products' not in st.session_state:
    st.session_state.products = {}

def fetch_sales():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            return response.json()
        st.error(f"Failed to fetch sales: {response.status_code} - {response.text}")
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

def create_sale(sale_data):
    try:
        response = requests.post(BASE_URL, json=sale_data)
        if response.status_code == 201:
            return True
        st.error(f"Failed to create sale: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        st.error(f"API connection failed: {e}")
        return False

def update_sale(sale_id, sale_data):
    try:
        response = requests.put(f"{BASE_URL}{sale_id}/", json=sale_data)
        if response.status_code == 200:
            return True
        st.error(f"Failed to update sale: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        st.error(f"API connection failed: {e}")
        return False

def delete_sale(sale_id):
    try:
        response = requests.delete(f"{BASE_URL}{sale_id}/")
        if response.status_code == 204:
            return True
        st.error(f"Failed to delete sale: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        st.error(f"API connection failed: {e}")
        return False

# Load products data
products_data = fetch_products()
if products_data:
    st.session_state.products = {product['id']: product['name'] for product in products_data}

# Load and prepare sales data
sales_data = fetch_sales()
df = pd.DataFrame()

if sales_data:
    df = pd.DataFrame(sales_data)
    # Replace product IDs with names
    df['product'] = df['product'].map(st.session_state.products)
    column_mapping = {
        'date': 'Date',
        'customer': 'Customer',
        'product': 'Product',
        'amount': 'Amount',
        'notes': 'Notes',
        'id': 'ID'
    }
    df = df.rename(columns=column_mapping)
else:
    df = pd.DataFrame(columns=["ID", "Date", "Customer", "Product", "Amount", "Notes"])

# UI Components
st.title("💰 Sales")

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
    df[['Date', 'Customer', 'Product', 'Amount', 'Notes']],
    use_container_width=True,
    hide_index=True,
    height=min(210, 35 * (len(df) + 1))
)

# Success Messages
if st.session_state.show_add_success:
    st.success("Sale Added Successfully!")
    st.session_state.show_add_success = False

if st.session_state.show_update_success:
    st.success("Sale Updated Successfully!")
    st.session_state.show_update_success = False

if st.session_state.show_delete_success:
    st.success("Sale Deleted Successfully!")
    st.session_state.show_delete_success = False

# Action Section
st.divider()
st.write("#### ➕✏️🗑️ Actions:")
st.write("")

col_a, col_b = st.columns([2,5])

# Add Sale Form
with col_a:
    if st.button("➕ Add New Sale"):
        st.session_state.show_add_form = True
        st.session_state.show_edit_form = False
        st.session_state.show_delete_confirm = False
        st.rerun()

if st.session_state.show_add_form:
    with st.form("add_sale_form"):
        st.subheader("Add New Sale Details")
        date = st.date_input("Date*", value=datetime.now())
        customer = st.text_input("Customer", placeholder="Optional customer name")
        
        # Create product selection dropdown
        product_options = {product['id']: product['name'] for product in products_data} if products_data else {}
        selected_product_id = st.selectbox(
            "Product*",
            options=list(product_options.keys()),
            format_func=lambda x: product_options[x]
        )
        
        amount = st.number_input("Amount*", min_value=1, value=1)
        notes = st.text_area("Notes", placeholder="Optional notes about the sale")

        col1, col2 = st.columns(2)
        submitted = col1.form_submit_button("✅ Save Sale")
        cancel = col2.form_submit_button("❌ Cancel")

        if submitted:
            new_sale = {
                'date': str(date),
                'customer': customer,
                'product': selected_product_id,
                'amount': amount,
                'notes': notes
            }

            if create_sale(new_sale):
                st.session_state.show_add_success = True
                st.session_state.show_add_form = False
                st.rerun()

        if cancel:
            st.session_state.show_add_form = False
            st.rerun()

# Edit/Delete Sale Section
with col_b:
    if not df.empty:    
        sale_options = ["Select a sale to edit or delete"] + [
            f"{row['Date']} - {row['Customer']} - {row['Product']} ({row['Amount']})" 
            for _, row in df.iterrows()
        ]
        
        selected_sale = st.selectbox(
            "hidden",
            options=sale_options,
            key="sale_selection",
        )

        selected_sale_data = None
        if selected_sale != "Select a sale to edit or delete":
            parts = selected_sale.split(" - ")
            selected_date = parts[0]
            selected_customer = parts[1]
            selected_product = parts[2].split(" (")[0]
            selected_amount = parts[2].split(" (")[1].rstrip(")")
            
            matching_sales = df[
                (df['Date'] == selected_date) & 
                (df['Customer'] == selected_customer) &
                (df['Product'] == selected_product) &
                (df['Amount'].astype(str) == selected_amount)
            ]
            
            if not matching_sales.empty:
                selected_sale_data = matching_sales.iloc[0]
                st.session_state.selected_sale_id = selected_sale_data['ID']

        if selected_sale_data is not None:
            st.write("")
            col_edit, col_delete = st.columns(2)

            if col_edit.button(f"✏️ Edit Sale"):
                st.session_state.show_edit_form = True
                st.session_state.show_delete_confirm = False
                st.session_state.show_add_form = False
                st.rerun()

            if col_delete.button(f"🗑️ Delete Sale"):
                st.session_state.show_delete_confirm = True
                st.session_state.show_edit_form = False
                st.session_state.show_add_form = False
                st.rerun()

    # Edit Sale Form
    if st.session_state.show_edit_form and selected_sale_data is not None:
        st.write("---")
        with st.form("edit_sale_form"):
            st.subheader(f"Edit Sale: {selected_sale_data['Product']}")
            
            # Convert date string back to date object
            edit_date = st.date_input(
                "Date*", 
                value=datetime.strptime(selected_sale_data['Date'], '%Y-%m-%d')
            )
            edit_customer = st.text_input(
                "Customer", 
                value=selected_sale_data['Customer']
            )
            
            # Product selection for edit
            current_product_id = [
                pid for pid, name in st.session_state.products.items() 
                if name == selected_sale_data['Product']
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
                value=int(selected_sale_data['Amount'])
            )
            edit_notes = st.text_area(
                "Notes", 
                value=selected_sale_data['Notes']
            )

            col_edit_submit, col_edit_cancel = st.columns(2)
            edit_submitted = col_edit_submit.form_submit_button("💾 Save Changes")
            edit_cancel = col_edit_cancel.form_submit_button("❌ Cancel Edit")

            if edit_submitted:
                updated_sale = {
                    'date': str(edit_date),
                    'customer': edit_customer,
                    'product': edit_product_id,
                    'amount': edit_amount,
                    'notes': edit_notes
                }
                
                if update_sale(st.session_state.selected_sale_id, updated_sale):
                    st.session_state.show_update_success = True
                    st.session_state.show_edit_form = False
                    st.session_state.selected_sale_id = None
                    st.rerun()

            if edit_cancel:
                st.session_state.show_edit_form = False
                st.session_state.selected_sale_id = None
                st.rerun()

    # Delete Confirmation
    if st.session_state.show_delete_confirm and selected_sale_data is not None:
        st.warning(f"Are you sure you want to delete the sale of **{selected_sale_data['Amount']} {selected_sale_data['Product']}** on **{selected_sale_data['Date']}**? This action cannot be undone.")
        col_del_confirm, col_del_cancel = st.columns(2)

        if col_del_confirm.button("🗑️ Yes, Delete Sale"):
            if delete_sale(st.session_state.selected_sale_id):
                st.session_state.show_delete_success = True
                st.session_state.show_delete_confirm = False
                st.session_state.selected_sale_id = None
                st.rerun()
        if col_del_cancel.button("❌ Cancel Deletion"):
            st.session_state.show_delete_confirm = False
            st.session_state.selected_sale_id = None
            st.rerun()