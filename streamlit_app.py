import streamlit as st

st.title("🖥️ Smart Inventory Dashboard")
st.markdown("""
Welcome to your inventory management system! Navigate using the sidebar.
""")

# Sidebar navigation
st.sidebar.title("🏢 Smart Inventory")
st.sidebar.divider()
st.sidebar.page_link("streamlit_app.py", label="🏠 Home")
st.sidebar.page_link("pages/1_Inventory.py", label="📦 Inventory")
st.sidebar.page_link("pages/2_Purchases.py", label="🛒 Purchases")
st.sidebar.page_link("pages/3_Sales.py", label="💰 Sales")
st.sidebar.page_link("pages/4_AI_Assistant.py", label="🤖 AI Assistant")
