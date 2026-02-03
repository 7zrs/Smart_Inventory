import streamlit as st
import pandas as pd
import requests
from Pages.login import handle_logout

# Check if user is authenticated
if 'auth' not in st.session_state or not st.session_state.auth.get('authenticated', False):
    st.switch_page("pages/login.py")
    st.stop()

BASE_URL = "http://127.0.0.1:8000/api/products/"

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

# Initialize session state
if 'show_add_success' not in st.session_state:
    st.session_state.show_add_success = False
if 'show_update_success' not in st.session_state:
    st.session_state.show_update_success = False
if 'show_delete_success' not in st.session_state:
    st.session_state.show_delete_success = False
if 'selected_product_id' not in st.session_state:
    st.session_state.selected_product_id = None
if 'show_edit_dialog' not in st.session_state:
    st.session_state.show_edit_dialog = False
if 'show_delete_dialog' not in st.session_state:
    st.session_state.show_delete_dialog = False

def fetch_products():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            return response.json()
        st.error(f"Failed to fetch products: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        st.error(f"Failed to connect to the API: {e}")
        return None

def create_product(product_data):
    try:
        response = requests.post(BASE_URL, json=product_data)
        if response.status_code == 201:
            return True, None
        return False, f"Failed to create product: {response.status_code} - {response.text}"
    except Exception as e:
        return False, f"API connection failed: {e}"

def update_product(product_id, product_data):
    try:
        converted_data = {
            'name': str(product_data['name']),
            'unit': str(product_data['unit']),
            'notes': str(product_data['notes']),
            'purchased_amount': int(product_data['purchased_amount']),
            'sold_amount': int(product_data['sold_amount']),
            'stock_level': int(product_data['stock_level'])
        }
        response = requests.put(f"{BASE_URL}{product_id}/", json=converted_data)
        if response.status_code == 200:
            return True, None
        return False, f"Failed to update product: {response.status_code} - {response.text}"
    except Exception as e:
        return False, f"API connection failed: {e}"

def delete_product(product_id):
    try:
        response = requests.delete(f"{BASE_URL}{product_id}/")
        if response.status_code == 204:
            return True, None
        return False, f"Failed to delete product: {response.status_code} - {response.text}"
    except Exception as e:
        return False, f"API connection failed: {e}"

def product_name_exists(name, exclude_id=None):
    """Check if a product name already exists (case-insensitive)"""
    if 'product_names' in st.session_state:
        for n, pid in st.session_state.product_names.items():
            if n.lower() == name.lower() and pid != exclude_id:
                return True
    return False


# Dialog for adding new product
@st.dialog("Add New Product")
def add_product_dialog():
    name = st.text_input("Product Name*", placeholder="Enter product name")
    unit = st.text_input("Unit*", placeholder="e.g., kg, liter, box")
    notes = st.text_area("Notes", placeholder="Optional notes about the product")

    col1, col2 = st.columns(2)
    if col1.button("✅ Save Product", use_container_width=True):
        if name and unit:
            if product_name_exists(name):
                st.error("Product name already exists!")
            else:
                new_product = {
                    'name': name,
                    'unit': unit,
                    'notes': notes,
                    'purchased_amount': 0,
                    'sold_amount': 0,
                    'stock_level': 0
                }
                success, error = create_product(new_product)
                if success:
                    st.session_state.show_add_success = True
                    st.rerun()
                else:
                    st.error(error)
        else:
            st.warning("Please fill in all required fields (marked with *)")

    if col2.button("❌ Cancel", use_container_width=True):
        st.rerun()


# Dialog for editing product
@st.dialog("Edit Product")
def edit_product_dialog(product_data, product_id):
    edit_name = st.text_input("Product Name*", value=product_data['Product'])
    edit_unit = st.text_input("Unit*", value=product_data['Unit'])
    edit_notes = st.text_area("Notes", value=product_data['Notes'] if product_data['Notes'] else "")

    if edit_name != product_data['Product'] and product_name_exists(edit_name, product_id):
        st.error("A product with this name already exists!")

    col1, col2 = st.columns(2)
    if col1.button("💾 Save Changes", use_container_width=True):
        if edit_name and edit_unit:
            if edit_name != product_data['Product'] and product_name_exists(edit_name, product_id):
                st.error("A product with this name already exists!")
            else:
                updated_product = {
                    'name': edit_name,
                    'unit': edit_unit,
                    'notes': edit_notes,
                    'purchased_amount': int(product_data['Purchased Amt']),
                    'sold_amount': int(product_data['Sold Amt']),
                    'stock_level': int(product_data['Stock Level']),
                }
                success, error = update_product(product_id, updated_product)
                if success:
                    st.session_state.show_update_success = True
                    st.session_state.show_edit_dialog = False
                    st.session_state.selected_product_id = None
                    st.rerun()
                else:
                    st.error(error)
        else:
            st.warning("Please fill in all required fields (marked with *)")

    if col2.button("❌ Cancel", use_container_width=True):
        st.session_state.show_edit_dialog = False
        st.session_state.selected_product_id = None
        st.rerun()


# Dialog for delete confirmation
@st.dialog("Confirm Delete")
def delete_product_dialog(product_name, product_id):
    st.warning(f"Are you sure you want to delete **'{product_name}'**?")
    st.caption("This action cannot be undone.")

    col1, col2 = st.columns(2)
    if col1.button("🗑️ Yes, Delete", use_container_width=True, type="primary"):
        success, error = delete_product(product_id)
        if success:
            st.session_state.show_delete_success = True
            st.session_state.show_delete_dialog = False
            st.session_state.selected_product_id = None
            st.rerun()
        else:
            st.error(error)

    if col2.button("❌ Cancel", use_container_width=True):
        st.session_state.show_delete_dialog = False
        st.session_state.selected_product_id = None
        st.rerun()


# Load and prepare data
inventory_data = fetch_products()
df = pd.DataFrame()

if inventory_data:
    df = pd.DataFrame(inventory_data)
    st.session_state.product_names = {product['name']: product['id'] for product in inventory_data}
    column_mapping = {
        'name': 'Product',
        'unit': 'Unit',
        'purchased_amount': 'Purchased Amt',
        'sold_amount': 'Sold Amt',
        'stock_level': 'Stock Level',
        'notes': 'Notes',
        'id': 'ID'
    }
    df = df.rename(columns=column_mapping)
else:
    df = pd.DataFrame(columns=["ID", "Product", "Unit", "Purchased Amt", "Sold Amt", "Stock Level", "Notes"])

# UI Components
st.title("📦 Inventory")

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

st.dataframe(
    df[['Product', 'Unit', 'Purchased Amt', 'Sold Amt', 'Stock Level', 'Notes']],
    use_container_width=True,
    hide_index=True,
    height=min(210, 35 * (len(df) + 1))
)

# Success Messages
if st.session_state.show_add_success:
    st.success("Product Added Successfully!")
    st.session_state.show_add_success = False

if st.session_state.show_update_success:
    st.success("Product Updated Successfully!")
    st.session_state.show_update_success = False

if st.session_state.show_delete_success:
    st.success("Product Deleted Successfully!")
    st.session_state.show_delete_success = False

# Action Section
st.divider()
st.write("#### ➕✏️🗑️ Actions:")
st.write("")

col_a, col_b = st.columns([2, 5])

# Add Product Button
with col_a:
    if st.button("➕ Add New Product"):
        add_product_dialog()

# Edit/Delete Product Section
with col_b:
    if not df.empty:
        product_names_list = ["Select a product to edit or delete"] + list(st.session_state.product_names.keys())
        selected_product_name = st.selectbox(
            "hidden",
            options=product_names_list,
            key="product_selection",
            label_visibility="collapsed"
        )

        selected_product_data = None
        if selected_product_name != "Select a product to edit or delete":
            selected_product_id = st.session_state.product_names[selected_product_name]
            st.session_state.selected_product_id = selected_product_id
            selected_product_data = df[df['ID'] == selected_product_id].iloc[0]

        if selected_product_data is not None:
            st.write("")
            col_edit, col_delete = st.columns(2)

            with col_edit:
                if st.button(f"✏️ Edit '{selected_product_name}'"):
                    st.session_state.show_edit_dialog = True

            with col_delete:
                if st.button(f"🗑️ Delete '{selected_product_name}'"):
                    st.session_state.show_delete_dialog = True

# Show dialogs based on state
if st.session_state.show_edit_dialog and st.session_state.selected_product_id:
    product_data = df[df['ID'] == st.session_state.selected_product_id].iloc[0]
    edit_product_dialog(product_data, st.session_state.selected_product_id)

if st.session_state.show_delete_dialog and st.session_state.selected_product_id:
    product_name = df[df['ID'] == st.session_state.selected_product_id].iloc[0]['Product']
    delete_product_dialog(product_name, st.session_state.selected_product_id)
