import streamlit as st
from Pages.login import handle_logout

# Check if user is authenticated 
if 'auth' not in st.session_state or not st.session_state.auth.get('authenticated', False):
    # Redirect to login page
    st.switch_page("pages/login.py")  
    st.stop()  # Stop execution of the rest of the page

st.title("🖥️ Smart Inventory")
st.divider()

# Welcome Section
st.markdown(f"### 👋 Welcome, {st.session_state.auth['username']}!")
st.write("")

# Project Summary
st.markdown("#### About This System")
st.markdown("""
**Smart Inventory** is a streamlined inventory management system that enables users to add, edit,
delete, and view products, as well as record incoming shipments and outgoing sales transactions.
The system provides efficient management of product data and inventory flow, along with the ability
to generate reports for tracking stock levels, sales history, and shipment details including
material movements, dates, and quantities.

The system is enhanced with a **Large Language Model (LLM)** to provide a natural language
conversational interface, laying the foundation for an improved user experience in inventory
management. Users can perform core operations and generate reports through simple text interactions,
while still having access to traditional interface options. The system is designed with scalability
in mind, allowing for future enhancements and additional features.
""")

st.divider()

# Instructions Section
st.markdown("#### How to Use This System")
st.caption("Click on each section below to learn more")

with st.expander("📦 **Inventory Management** - Manage your products", expanded=False):
    st.markdown("""
    The Inventory page is your central hub for managing all products in the system.

    | Action | How to Do It |
    |--------|--------------|
    | **Add Product** | Click the `Add New Product` button and fill in the product details |
    | **Edit Product** | Select a product from the dropdown, then click `Edit` |
    | **Delete Product** | Select a product from the dropdown, then click `Delete` |

    > **Tip:** The dropdown has a smart search filter - just start typing to find items quickly!
    """)

with st.expander("🛒 **Purchases** - Record incoming inventory", expanded=False):
    st.markdown("""
    Track all incoming stock from your suppliers on the Purchases page.

    | Action | How to Do It |
    |--------|--------------|
    | **Add Purchase** | Click `Add New Purchase`, select product, enter quantity and supplier |
    | **Edit Purchase** | Select a purchase from the dropdown, then click `Edit` |
    | **Delete Purchase** | Select a purchase from the dropdown, then click `Delete` |

    > **Tip:** The dropdown has a smart search filter - just start typing to find items quickly!
    """)

with st.expander("💰 **Sales** - Track outgoing transactions", expanded=False):
    st.markdown("""
    Record all sales transactions and customer information on the Sales page.

    | Action | How to Do It |
    |--------|--------------|
    | **Add Sale** | Click `Add New Sale`, select product, enter quantity and customer |
    | **Edit Sale** | Select a sale from the dropdown, then click `Edit` |
    | **Delete Sale** | Select a sale from the dropdown, then click `Delete` |

    > **Tip:** The dropdown has a smart search filter - just start typing to find items quickly!
    """)

with st.expander("🤖 **AI Assistant** - Natural language queries", expanded=False):
    st.markdown("""
    Use the AI Assistant to interact with your data using natural language.

    **Example Commands:**
    - "Show me all products with low stock"
    - "Add a new product called Laptop with unit piece"
    - "Delete the sale with ID 5"
    - "Which product has the highest stock level?"

    > **Tip:** You can ask questions, add new records, or delete existing ones - just describe what you need!
    **Use any language or dialect you like!**
    """)

st.divider()

# Tips Section
st.markdown("#### Quick Tips")
col_tip1, col_tip2, col_tip3 = st.columns(3)

with col_tip1:
    st.info("**Start with Products**\n\nAlways add products first before recording purchases or sales.")

with col_tip2:
    st.info("**Use Notes**\n\nKeep detailed notes for better tracking and future reference.")

with col_tip3:
    st.info("**Try AI Assistant**\n\nAsk questions naturally to quickly find the information you need.")

st.divider()

# Credits Section
st.markdown("#### Project Credits")

credits_col1, credits_col2, credits_col3 = st.columns([1, 2, 1])

with credits_col2:

    dev_col1, dev_col2 = st.columns(2)
    with dev_col1:
        st.markdown("**Hasan Zidan**")
        st.caption("hasan_171117")
    with dev_col2:
        st.markdown("**Ali Al_Ali**")
        st.caption("ali_171119")

    st.caption("Syrian Virtual University - BPR601")

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
