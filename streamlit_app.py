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
if 'show_success' not in st.session_state:
    st.session_state.show_success = False

# Custom CSS
st.markdown("""
<style>
    /* Make radio buttons bigger */
    div[role=radiogroup] label {
        padding: 10px 15px;
        font-size: 18px;
        margin: 5px 0;
    }
    
    /* Center the AI chat button */
    div[data-testid="stSidebar"] div:has(> .element-container > .stButton > button) {
        display: flex;
        justify-content: center;
    }
    
    /* Style the AI chat button */
    .ai-chat-button {
        background-color: #4CAF50;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        cursor: pointer;
        border-radius: 12px;
        border: none;
        width: 90%;
        transition: background-color 0.3s;
    }
    .ai-chat-button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with tabs and AI chat button
st.sidebar.title("Smart Inventory")
st.sidebar.divider()

col1, col2, col3 = st.sidebar.columns([1, 9, 1])
with col2:
    tab = st.radio("",
        ["📦 Inventory", "🛒 Purchases", "💰 Sales"],
        key="main_tabs"
    )

# AI Chat button in sidebar
st.sidebar.divider()
col1, col2, col3 = st.sidebar.columns([1, 8, 1])  # Changed from [1,9,1] to [1,8,1] for better centering
with col2:
    if st.button("🤖 Start AI Chat", use_container_width=True):
        tab = "💬 AI Assistant"

# Main page content
if tab == "📦 Inventory":
    st.title("Inventory")
    
    if st.session_state.show_success:
        st.success("Changes saved successfully!")
        st.session_state.show_success = False
    
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

elif tab == "🛒 Purchases":
    st.title("Purchases")

elif tab == "💰 Sales":
    st.title("Sales")

elif tab == "💬 AI Assistant":
    st.title("AI Assistant")
    st.markdown("### Control your inventory with natural language")
    
    # Chat interface
    user_input = st.text_area("Ask about stock, add notes, or get insights...", 
                             height=150)
    col1, col2 = st.columns([1, 0.2])
    if col1.button("Send Message"):
        if user_input.strip():
            st.success(f"AI: I received your message: '{user_input}'")
        else:
            st.warning("Please enter a message first")
    
    if col2.button("Clear"):
        st.rerun()
    
    # Example questions
    st.markdown("### Try asking:")
    st.markdown("- What's my current stock level for Milk?")
    st.markdown("- Add a note to Apples: 'Order more next week'")
    st.markdown("- Which items need restocking?")