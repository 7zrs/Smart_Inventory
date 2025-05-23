import streamlit as st

# Sidebar navigation
st.sidebar.title("🏠 Smart Inventory")
st.sidebar.divider()
st.sidebar.page_link("streamlit_app.py", label="Home")
st.sidebar.page_link("pages/1_Inventory.py", label="📦 Inventory")
st.sidebar.page_link("pages/2_Purchases.py", label="🛒 Purchases")
st.sidebar.page_link("pages/3_Sales.py", label="💰 Sales")
st.sidebar.page_link("pages/4_AI_Assistant.py", label="🤖 AI Assistant")

st.title("🛒 Purchases")
st.write("Manage your purchase orders here.")
# Add purchase-related functionality here