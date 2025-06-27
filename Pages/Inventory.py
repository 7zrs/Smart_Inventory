import streamlit as st
import pandas as pd
import requests

BASE_URL = "http://127.0.0.1:8000/api/products/"

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
if 'selected_product_id' not in st.session_state:
    st.session_state.selected_product_id = None
if 'show_update_success' not in st.session_state:
    st.session_state.show_update_success = False
if 'show_delete_success' not in st.session_state:
    st.session_state.show_delete_success = False

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
            return True
        st.error(f"Failed to create product: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        st.error(f"API connection failed: {e}")
        return False

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
            return True
        st.error(f"Failed to update product: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        st.error(f"API connection failed: {e}")
        return False

def delete_product(product_id):
    try:
        response = requests.delete(f"{BASE_URL}{product_id}/")
        if response.status_code == 204:
            return True
        st.error(f"Failed to delete product: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        st.error(f"API connection failed: {e}")
        return False

def product_name_exists(name):
    """Check if a product name already exists (case-insensitive)"""
    if 'product_names' in st.session_state:
        return name.lower() in [n.lower() for n in st.session_state.product_names.keys()]
    return False

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

col_a, col_b = st.columns([2,5])

# Add Product Form
with col_a:
    if st.button("➕ Add New Product"):
        st.session_state.show_add_form = True
        st.session_state.show_edit_form = False
        st.session_state.show_delete_confirm = False
        st.rerun()

if st.session_state.show_add_form:
    with st.form("add_product_form"):
        st.subheader("Add New Product Details")
        name = st.text_input("Product Name*", placeholder="Enter product name", key="new_product_name")
        unit = st.text_input("Unit*", placeholder="e.g., kg, liter, box")
        notes = st.text_area("Notes", placeholder="Optional notes about the product")

        col1, col2 = st.columns(2)
        submitted = col1.form_submit_button("✅ Save Product")
        cancel = col2.form_submit_button("❌ Cancel")

        if submitted:
            if name and unit:
                if product_name_exists(name):
                    st.error("Cannot save: Product name already exists")
                else:
                    new_product = {
                        'name': name,
                        'unit': unit,
                        'notes': notes,
                        'purchased_amount': 0,
                        'sold_amount': 0,
                        'stock_level': 0
                    }

                    if create_product(new_product):
                        st.session_state.show_add_success = True
                        st.session_state.show_add_form = False
                        st.rerun()
            else:
                st.warning("Please fill in all required fields (marked with *)")

        if cancel:
            st.session_state.show_add_form = False
            st.rerun()

# Edit/Delete Product Section
with col_b:
    if not df.empty:    
        product_names_list = ["Select a product to edit or delete"] + list(st.session_state.product_names.keys())
        selected_product_name = st.selectbox(
            "hidden",
            options=product_names_list,
            key="product_selection",
        )

        selected_product_data = None
        if selected_product_name != "Select a product to edit or delete":
            selected_product_id = st.session_state.product_names[selected_product_name]
            st.session_state.selected_product_id = selected_product_id
            selected_product_data = df[df['ID'] == selected_product_id].iloc[0]

        if selected_product_data is not None:
            st.write("")
            col_edit, col_delete = st.columns(2)

            if col_edit.button(f"✏️ Edit '{selected_product_name}'"):
                st.session_state.show_edit_form = True
                st.session_state.show_delete_confirm = False
                st.session_state.show_add_form = False
                st.rerun()

            if col_delete.button(f"🗑️ Delete '{selected_product_name}'"):
                st.session_state.show_delete_confirm = True
                st.session_state.show_edit_form = False
                st.session_state.show_add_form = False
                st.rerun()

    # Edit Product Form
    if st.session_state.show_edit_form and selected_product_data is not None:
        st.write("---")
        with st.form("edit_product_form"):
            st.subheader(f"Edit Product: {selected_product_data['Product']}")
            edit_name = st.text_input("Product Name*", value=selected_product_data['Product'])
            edit_unit = st.text_input("Unit*", value=selected_product_data['Unit'])
            edit_notes = st.text_area("Notes", value=selected_product_data['Notes'])

            # Show warning if name is changed to an existing one
            if (edit_name != selected_product_data['Product'] and 
                product_name_exists(edit_name)):
                st.error("A product with this name already exists. Please choose a different name.")

            col_edit_submit, col_edit_cancel = st.columns(2)
            edit_submitted = col_edit_submit.form_submit_button("💾 Save Changes")
            edit_cancel = col_edit_cancel.form_submit_button("❌ Cancel Edit")

            if edit_submitted:
                if edit_name and edit_unit:
                    if not (edit_name != selected_product_data['Product'] and 
                        product_name_exists(edit_name)):
                        updated_product = {
                            'name': edit_name,
                            'unit': edit_unit,
                            'notes': edit_notes,
                            'purchased_amount': int(selected_product_data['Purchased Amt']),
                            'sold_amount': int(selected_product_data['Sold Amt']),
                            'stock_level': int(selected_product_data['Stock Level']),
                        }
                        if update_product(st.session_state.selected_product_id, updated_product):
                            st.session_state.show_update_success = True
                            st.session_state.show_edit_form = False
                            st.session_state.selected_product_id = None
                            st.rerun()
                else:
                    st.warning("Please fill in all required fields (marked with *)")

            if edit_cancel:
                st.session_state.show_edit_form = False
                st.session_state.selected_product_id = None
                st.rerun()

    # Delete Confirmation
    if st.session_state.show_delete_confirm and selected_product_data is not None:
        st.warning(f"Are you sure you want to delete **'{selected_product_data['Product']}'**? This action cannot be undone.")
        col_del_confirm, col_del_cancel = st.columns(2)

        if col_del_confirm.button("🗑️ Yes, Delete Product"):
            if delete_product(st.session_state.selected_product_id):
                st.session_state.show_delete_success = True
                st.session_state.show_delete_confirm = False
                st.session_state.selected_product_id = None
                st.rerun()
        if col_del_cancel.button("❌ Cancel Deletion"):
            st.session_state.show_delete_confirm = False
            st.session_state.selected_product_id = None
            st.rerun()