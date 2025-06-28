import streamlit as st
import requests
import json
from llm_utilities.utils import process_user_input, confirm_and_execute_tasks

# Sidebar navigation
st.sidebar.title("🏢 Smart Inventory")
st.sidebar.divider()
st.sidebar.page_link("streamlit_app.py", label="🏠 Home")
st.sidebar.page_link("pages/Inventory.py", label="📦 Inventory")
st.sidebar.page_link("pages/Purchases.py", label="🛒 Purchases")
st.sidebar.page_link("pages/Sales.py", label="💰 Sales")
st.sidebar.page_link("pages/AI_Assistant.py", label="🤖 AI Assistant")

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
        
        col1, col2 = st.columns(2)
        if col1.button("✅ Yes", key="confirm_task"):
            try:
                # Execute just the current task
                confirm_and_execute_tasks([task])
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"Action completed: {task['confirmation_message'][16:].split('.')[0]}"
                })
                
                # Move to next task or clear if done
                if st.session_state.current_task_index + 1 < len(st.session_state.pending_tasks):
                    st.session_state.current_task_index += 1
                else:
                    st.session_state.pending_tasks = []
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
        
        if col2.button("❌ No", key="cancel_task"):
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"Action cancelled: {task['confirmation_message'][16:].split('.')[0]}"
            })
            # Move to next task or clear if done
            if st.session_state.current_task_index + 1 < len(st.session_state.pending_tasks):
                st.session_state.current_task_index += 1
            else:
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