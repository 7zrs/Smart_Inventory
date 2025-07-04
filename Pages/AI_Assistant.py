import streamlit as st
import requests
import json
from llm_utilities.utils import process_user_input, confirm_and_execute_tasks
from Pages.login import handle_logout

# Check if user is authenticated 
if 'auth' not in st.session_state or not st.session_state.auth.get('authenticated', False):
    # Redirect to login page
    st.switch_page("pages/login.py")  
    st.stop()  # Stop execution of the rest of the page

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

st.title("🤖 AI Assistant")
st.markdown("### Control your inventory with natural language")

# Initialize chat history and task state in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_tasks" not in st.session_state:
    st.session_state.pending_tasks = []
if "current_task_index" not in st.session_state:
    st.session_state.current_task_index = None

def fetch_products():
    try:
        response = requests.get("http://127.0.0.1:8000/api/products/")
        if response.status_code == 200:
            return response.json()
        st.error(f"Failed to fetch products: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        st.error(f"Failed to connect to the API: {e}")
        return None

def fetch_purchases():
    try:
        response = requests.get("http://127.0.0.1:8000/api/purchases/")
        if response.status_code == 200:
            return response.json()
        st.error(f"Failed to fetch purchases: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        st.error(f"Failed to connect to the API: {e}")
        return None

def fetch_sales():
    try:
        response = requests.get("http://127.0.0.1:8000/api/sales/")
        if response.status_code == 200:
            return response.json()
        st.error(f"Failed to fetch sales: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        st.error(f"Failed to connect to the API: {e}")
        return None

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Display pending task confirmation if exists
if st.session_state.pending_tasks and st.session_state.current_task_index is not None:
    task = st.session_state.pending_tasks[st.session_state.current_task_index]
    with st.chat_message("assistant"):
        st.markdown(task["confirmation_message"])
        
        # Show task navigation and count
        task_count = len(st.session_state.pending_tasks)
        current_task_num = st.session_state.current_task_index + 1
        st.caption(f"Task {current_task_num} of {task_count}")
        
        # Navigation buttons
        nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
        
        if nav_col1.button("⏮️ First", key="first_task"):
            st.session_state.current_task_index = 0
            st.rerun()
            
        if nav_col2.button("⏪ Previous", key="prev_task") and st.session_state.current_task_index > 0:
            st.session_state.current_task_index -= 1
            st.rerun()
            
        if nav_col3.button("⏩ Next", key="next_task") and st.session_state.current_task_index < len(st.session_state.pending_tasks) - 1:
            st.session_state.current_task_index += 1
            st.rerun()
            
        if nav_col4.button("⏭️ Last", key="last_task"):
            st.session_state.current_task_index = len(st.session_state.pending_tasks) - 1
            st.rerun()
        
        # Confirmation buttons - now with 4 columns for Cancel This
        col1, col2, col3, col4 = st.columns(4)
        
        if col1.button("✅ Confirm This", key="confirm_task"):
            try:
                # Execute just the current task
                confirm_and_execute_tasks([task])
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"✅ Action completed: {task['confirmation_message'][16:].split('.')[0]}"
                })
                
                # Remove the completed task
                st.session_state.pending_tasks.pop(st.session_state.current_task_index)
                
                # Adjust index or clear if no more tasks
                if st.session_state.pending_tasks:
                    if st.session_state.current_task_index >= len(st.session_state.pending_tasks):
                        st.session_state.current_task_index = len(st.session_state.pending_tasks) - 1
                else:
                    st.session_state.current_task_index = None
                st.rerun()
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"Error executing action: {str(e)}"
                })
                st.session_state.pending_tasks = []
                st.session_state.current_task_index = None
                st.rerun()
        
        if col2.button("✅ Confirm All", key="confirm_all"):
            try:
                # Execute all pending tasks
                confirm_and_execute_tasks(st.session_state.pending_tasks)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"✅ Completed {len(st.session_state.pending_tasks)} actions"
                })
                st.session_state.pending_tasks = []
                st.session_state.current_task_index = None
                st.rerun()
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"Error executing actions: {str(e)}"
                })
                st.session_state.pending_tasks = []
                st.session_state.current_task_index = None
                st.rerun()
        
        if col3.button("❌ Cancel This", key="cancel_this"):
            cancelled_task = st.session_state.pending_tasks.pop(st.session_state.current_task_index)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"❌ Action cancelled: {cancelled_task['confirmation_message'][16:].split('.')[0]}"
            })
            
            # Adjust index or clear if no more tasks
            if st.session_state.pending_tasks:
                if st.session_state.current_task_index >= len(st.session_state.pending_tasks):
                    st.session_state.current_task_index = len(st.session_state.pending_tasks) - 1
            else:
                st.session_state.current_task_index = None
            st.rerun()
        
        if col4.button("❌ Cancel All", key="cancel_all"):
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"❌ Cancelled {len(st.session_state.pending_tasks)} pending actions"
            })
            st.session_state.pending_tasks = []
            st.session_state.current_task_index = None
            st.rerun()

# Chat interface
user_input = st.chat_input("Ask about stock, add notes, or get insights...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Process the user input
    try:
        products = fetch_products()
        purchases = fetch_purchases()
        sales = fetch_sales()
        input_with_data = (
            user_input + "\nYou can make use of my current data:"
            "\nProducts:\n" + "\n".join(str(item) for item in products) +
            "\nPurchases:\n" + "\n".join(str(item) for item in purchases) +
            "\nSales:\n" + "\n".join(str(item) for item in sales)
        )
        tasks = process_user_input(input_with_data)
        
        if tasks:
            # Separate confirmation tasks from non-confirmation tasks
            confirmation_tasks = [task for task in tasks if task.get("confirmation_message")]
            non_confirmation_tasks = [task for task in tasks if not task.get("confirmation_message")]
            
            # Handle non-confirmation tasks first (like search results)
            if non_confirmation_tasks:
                with st.chat_message("assistant"):
                    for task in non_confirmation_tasks:
                        response = task.get("api_action")
                        response_content = requests.get("http://127.0.0.1:8000/"+response.split(" ")[1])
                        data = response_content.json()
                        if isinstance(data, list) and len(data) > 0:
                            # Get all keys except the first column
                            columns = list(data[0].keys())[1:]  # Skip first column
                            
                            # Build markdown table header
                            markdown_text = "| " + " | ".join(columns) + " |\n"
                            markdown_text += "| " + " | ".join(["---"] * len(columns)) + " |\n"
                            
                            # Add rows (keeping all rows but skipping first column in each)
                            for row in data:
                                values = list(row.values())[1:]  # Skip first column value
                                markdown_text += "| " + " | ".join(str(v) for v in values) + " |\n"
                            
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": markdown_text
                            })
                        else:
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": "No data found"
                            })
            
            # Handle confirmation tasks if any
            if confirmation_tasks:
                st.session_state.pending_tasks = confirmation_tasks
                st.session_state.current_task_index = 0
                st.rerun()
            else:
                st.rerun()
        else:
            # Handle cases where no tasks were generated
            with st.chat_message("assistant"):
                response = "I'm not sure what you mean. Could you clarify?"
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response
                })
                st.rerun()

    except Exception as e:
        with st.chat_message("assistant"):
            error_msg = f"An error occurred: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": error_msg
            })

# Example questions
st.markdown("### Try asking:")
st.markdown("- What's my current stock level for Milk?")
st.markdown("- Add a note to Apples: 'Order more next week'")
st.markdown("- Which items need restocking?")
st.markdown("- Add a new product named Laptop with unit pieces")
st.markdown("- Show all products with low stock (less than 10)")
st.markdown("- Record a purchase of 5 Laptops from SupplierX")