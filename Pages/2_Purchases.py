import streamlit as st
import pandas as pd
from datetime import datetime, date

# Sidebar navigation
st.sidebar.title("🏢 Smart Inventory")
st.sidebar.divider()
st.sidebar.page_link("streamlit_app.py", label="🏠 Home")
st.sidebar.page_link("pages/1_Inventory.py", label="📦 Inventory")
st.sidebar.page_link("pages/2_Purchases.py", label="🛒 Purchases")
st.sidebar.page_link("pages/3_Sales.py", label="💰 Sales")
st.sidebar.page_link("pages/4_AI_Assistant.py", label="🤖 AI Assistant")

# Initialize session state for purchases
if 'purchases_data' not in st.session_state:
    st.session_state.purchases_data = pd.DataFrame({
        "id": [1, 2],
        "date": [datetime(2023, 1, 1), datetime(2023, 1, 15)],  # Using datetime instead of date
        "supplier": ["Fresh Farms", "Dairy Co"],
        "product": [1, 2],
        "amount": [100, 50],
        "notes": ["Bulk order", "Monthly delivery"]
    })

if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

if 'show_success' not in st.session_state:
    st.session_state.show_success = False

# Page Title
st.title("🛒 Purchases")

if st.session_state.show_success:
    st.success("Changes saved successfully!")
    st.session_state.show_success = False

# Get product names for dropdown
product_options = {}
if 'inventory_data' in st.session_state:
    product_options = {idx: row['Product'] for idx, row in st.session_state.inventory_data.iterrows()}

# Convert date columns to datetime if they're in date format
if not st.session_state.purchases_data.empty and hasattr(st.session_state.purchases_data['date'].iloc[0], 'date'):
    st.session_state.purchases_data['date'] = pd.to_datetime(st.session_state.purchases_data['date'])

# Data Editor
edited_df = st.data_editor(
    st.session_state.purchases_data,
    column_config={
        "id": {"editable": False},
        "date": st.column_config.DateColumn(
            "Date",
            format="YYYY-MM-DD",
        ),
        "supplier": {"editable": st.session_state.edit_mode},
        "product": st.column_config.SelectboxColumn(
            "Product",
            options=product_options,
        ),
        "amount": {"editable": st.session_state.edit_mode},
        "notes": {"editable": st.session_state.edit_mode}
    },
    num_rows="dynamic",
    use_container_width=True,
    key="purchases_editor",
    disabled=not st.session_state.edit_mode
)

# Buttons
col1, col2 = st.columns(2)
if col1.button("➕ Add New Purchase"):
    st.session_state.edit_mode = True
    new_id = max(st.session_state.purchases_data['id']) + 1 if len(st.session_state.purchases_data) > 0 else 1
    new_row = {
        "id": new_id,
        "date": datetime.now(),  # Using datetime instead of date
        "supplier": "",
        "product": list(product_options.keys())[0] if product_options else 0,
        "amount": 0,
        "notes": ""
    }
    edited_df = pd.concat([edited_df, pd.DataFrame([new_row])], ignore_index=True)
    st.session_state.purchases_data = edited_df
    st.rerun()

if not st.session_state.edit_mode:
    if col2.button("✏️ Enable Edit"):
        st.session_state.edit_mode = True
        st.rerun()
else:
    if col2.button("💾 Save Changes"):
        # Ensure date column is in datetime format
        st.session_state.purchases_data = edited_df
        st.session_state.purchases_data['date'] = pd.to_datetime(st.session_state.purchases_data['date'])
        st.session_state.edit_mode = False
        st.session_state.show_success = True
        st.rerun()