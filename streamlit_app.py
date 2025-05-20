import streamlit as st
import pandas as pd

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
if 'show_success' not in st.session_state:  # New state for success message
    st.session_state.show_success = False

# Sidebar with tabs
st.sidebar.title("Smart Inventory")
tab = st.sidebar.radio("", ["📦 Inventory", "🛒 Purchases", "💰 Sales"])

# Main page (Inventory tab)
if tab == "📦 Inventory":
    st.title("Inventory")
    
    # Show success message if flag is set
    if st.session_state.show_success:
        st.success("Changes saved successfully!")
        st.session_state.show_success = False  # Reset the flag
    
    # Editable Table - only editable when in edit mode
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
    
    # Action buttons
    col1, col2 = st.columns(2)
    if col1.button("➕ Add New Product", disabled=not st.session_state.edit_mode):
        new_row = {"Product": "", "Unit": "", "Purchased Amt": 0, 
                  "Sold Amt": 0, "Stock Level": 0, "Notes": ""}
        edited_df.loc[len(edited_df)] = new_row
        st.session_state.inventory_data = edited_df
        st.rerun()
    
    # Edit/Save buttons
    if not st.session_state.edit_mode:
        if col2.button("✏️ Edit"):
            st.session_state.edit_mode = True
            st.rerun()
    else:
        if col2.button("💾 Save Changes"):
            st.session_state.inventory_data = edited_df
            st.session_state.edit_mode = False
            st.session_state.show_success = True  # Set flag to show message
            st.rerun()
    
    # Chat section
    st.subheader("Control via Chat")
    user_input = st.text_area("Ask about stock or add notes...")
    st.button("Send")

elif tab == "🛒 Purchases":
    st.title("Purchases")

elif tab == "💰 Sales":
    st.title("Sales")