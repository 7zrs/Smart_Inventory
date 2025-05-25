import streamlit as st

# Sidebar navigation
st.sidebar.title("🏢 Smart Inventory")
st.sidebar.divider()
st.sidebar.page_link("streamlit_app.py", label="🏠 Home")
st.sidebar.page_link("pages/1_Inventory.py", label="📦 Inventory")
st.sidebar.page_link("pages/2_Purchases.py", label="🛒 Purchases")
st.sidebar.page_link("pages/3_Sales.py", label="💰 Sales")
st.sidebar.page_link("pages/4_AI_Assistant.py", label="🤖 AI Assistant")

st.title("🤖 AI Assistant")
st.markdown("### Control your inventory with natural language")

# Chat interface
user_input = st.text_area("Ask about stock, add notes, or get insights...", height=150)

if  st.button("Send Message"):
    if user_input.strip():
        st.success(f"AI: I received your message: '{user_input}'")
    else:
        st.warning("Please enter a message first")

# Example questions
st.markdown("### Try asking:")
st.markdown("- What's my current stock level for Milk?")
st.markdown("- Add a note to Apples: 'Order more next week'")
st.markdown("- Which items need restocking?")