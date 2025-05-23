import streamlit as st
import pandas as pd

# Sidebar navigation
st.sidebar.title("🏠 Smart Inventory")
st.sidebar.divider()
st.sidebar.page_link("streamlit_app.py", label="Home")
st.sidebar.page_link("pages/1_Inventory.py", label="📦 Inventory")
st.sidebar.page_link("pages/2_Purchases.py", label="🛒 Purchases")
st.sidebar.page_link("pages/3_Sales.py", label="💰 Sales")
st.sidebar.page_link("pages/4_AI_Assistant.py", label="🤖 AI Assistant")

# Initialize session state 
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame({
        "Product": ["Apple", "Milk"],
        "Unit": ["kg", "L"],
        "Purchased Amt": [100, 50],
        "Sold Amt": [80, 40],
        "Stock Level": [20, 10],
        "Notes": ["Restock soon", "Good"]
    })

if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

if 'show_success' not in st.session_state:
    st.session_state.show_success = False

# Page Title
st.title("📦 Inventory")

if st.session_state.show_success:
    st.success("Changes saved successfully!")
    st.session_state.show_success = False

# Data Editor
edited_df = st.data_editor(
    st.session_state.inventory_data,
    column_config={
        "Product": {"editable": st.session_state.edit_mode},
        "Unit": {"editable": st.session_state.edit_mode},
        "Purchased Amt": {"editable": False},
        "Sold Amt": {"editable": False},
        "Stock Level": {"editable": False},
        "Notes": {"editable": st.session_state.edit_mode}
    },
    num_rows="dynamic",
    use_container_width=True,
    key="inventory_editor",
    disabled=not st.session_state.edit_mode
)

# Buttons
col1, col2 = st.columns(2)
if col1.button("➕ Add New Product"):
    st.session_state.edit_mode = True
    new_row = {"Product": "", "Unit": "", "Purchased Amt": 0, 
               "Sold Amt": 0, "Stock Level": 0, "Notes": ""}
    edited_df.loc[len(edited_df)] = new_row
    st.session_state.inventory_data = edited_df
    st.rerun()

if not st.session_state.edit_mode:
    if col2.button("✏️ Enable Edit"):
        st.session_state.edit_mode = True
        st.rerun()
else:
    if col2.button("💾 Save Changes"):
        st.session_state.inventory_data = edited_df
        st.session_state.edit_mode = False
        st.session_state.show_success = True
        st.rerun()