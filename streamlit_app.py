import streamlit as st
from Pages.login import handle_logout

# Check if user is authenticated 
if 'auth' not in st.session_state or not st.session_state.auth.get('authenticated', False):
    # Redirect to login page
    st.switch_page("pages/login.py")  
    st.stop()  # Stop execution of the rest of the page

st.title("🖥️ Smart Inventory")
st.divider()
st.markdown(f"#### 👋 Greetings {st.session_state.auth['username']}!")
st.write("")
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
st.sidebar.divider()
if st.sidebar.button("🚪 Logout"):
    handle_logout()
    st.switch_page("pages/login.py")

# Admin-only 
if st.session_state.auth.get('is_admin', False):
    if st.sidebar.button("↩️ Admin Dashboard"):
        st.switch_page("pages/login.py")
