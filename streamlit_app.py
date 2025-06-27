import streamlit as st

st.title("🖥️ Smart Inventory Dashboard")
st.markdown("""
Welcome to your inventory management system! Navigate using the sidebar.
""")

# Sidebar navigation
st.sidebar.title("🏢 Smart Inventory")
st.sidebar.divider()
st.sidebar.page_link("streamlit_app.py", label="🏠 Home")
st.sidebar.page_link("pages/Inventory.py", label="📦 Inventory")
st.sidebar.page_link("pages/Purchases.py", label="🛒 Purchases")
st.sidebar.page_link("pages/Sales.py", label="💰 Sales")
st.sidebar.page_link("pages/AI_Assistant.py", label="🤖 AI Assistant")
