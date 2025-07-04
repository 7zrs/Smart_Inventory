import streamlit as st
import requests
import json
from urllib.parse import urljoin
import base64

# Configuration
DJANGO_BASE_URL = "http://127.0.0.1:8000/"
LOGIN_URL = urljoin(DJANGO_BASE_URL, "login/")
LOGOUT_URL = urljoin(DJANGO_BASE_URL, "logout/")

# Set background image 
def set_background_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stForm {{
            background-color: rgba(14, 17, 23, 0.7); 
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1)
        }}
    
        /* Make expanders solid */
        .stExpander {{
            background-color: rgba(14, 17, 23, 0.7); 
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}   
        </style>
        """,
        unsafe_allow_html=True
    )

# Initialize the app with background
set_background_image("background.jpg")

def initialize_session_state():
    """Initialize all session state variables for authentication."""
    if 'auth' not in st.session_state:
        st.session_state.auth = {
            'authenticated': False,
            'username': None,
            'error': None,
            'success': None,
            'processing_login': False,
            'login_creds': {},
            'is_admin': False,
            'cookies': None
        }

def display_auth_messages():
    """Display authentication success/error messages and clear them."""
    if st.session_state.auth.get('error'):
        st.error(st.session_state.auth['error'])
        st.session_state.auth['error'] = None

    if st.session_state.auth.get('success'):
        st.success(st.session_state.auth['success'])
        st.session_state.auth['success'] = None

def handle_login(username, password):
    """Handle the login process with the Django backend."""
    st.session_state.auth['error'] = None
    st.session_state.auth['success'] = None

    try:
        response = requests.post(
            LOGIN_URL,
            data={'username': username, 'password': password},
            timeout=5
        )

        if 'application/json' in response.headers.get('Content-Type', ''):
            response_data = response.json()
        else:
            st.session_state.auth['error'] = f"Unexpected response from server (Status: {response.status_code}). Raw: {response.text[:200]}..."
            return

        if response.status_code == 200:
            auth_cookies = response.cookies
            role_response = requests.get(
                urljoin(DJANGO_BASE_URL, "check_role/"),
                cookies=auth_cookies,
                timeout=5
            )
            role_data = role_response.json()

            st.session_state.auth.update({
                'authenticated': True,
                'username': username,
                'is_admin': role_data.get('is_admin', False),
                'cookies': auth_cookies,
                'success': 'Login successful!'
            })
        else:
            st.session_state.auth['error'] = response_data.get('message', 'Login failed: Invalid credentials.')

    except requests.exceptions.Timeout:
        st.session_state.auth['error'] = "Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        st.session_state.auth['error'] = f"Could not connect to the Django backend at {DJANGO_BASE_URL}. Is it running?"
    except json.JSONDecodeError:
        st.session_state.auth['error'] = "Server returned invalid JSON response."
    except requests.exceptions.RequestException as e:
        st.session_state.auth['error'] = f"An error occurred during login: {str(e)}"

def handle_logout():
    """Handle the logout process with the Django backend."""
    st.session_state.auth['error'] = None
    st.session_state.auth['success'] = None

    try:
        response = requests.get(LOGOUT_URL, timeout=5)

        if 'application/json' in response.headers.get('Content-Type', ''):
            response_data = response.json()
        else:
            st.session_state.auth['error'] = f"Unexpected response from server (Status: {response.status_code}). Raw: {response.text[:200]}..."
            return

        if response.status_code == 200:
            if response_data.get('status') == 'success':
                st.session_state.auth.update({
                    'authenticated': False,
                    'username': None,
                    'is_admin': False,
                    'cookies': None,
                    'success': response_data.get('message', 'Logout successful.')
                })
            else:
                st.session_state.auth['error'] = response_data.get('message', 'Logout failed.')
        else:
            st.session_state.auth['error'] = response_data.get('message', f"Logout failed with status code: {response.status_code}")

    except requests.exceptions.Timeout:
        st.session_state.auth['error'] = "Request timed out during logout. Please try again."
    except requests.exceptions.ConnectionError:
        st.session_state.auth['error'] = f"Could not connect to the Django backend at {DJANGO_BASE_URL}. Is it running?"
    except json.JSONDecodeError:
        st.session_state.auth['error'] = "Server returned invalid JSON response during logout."
    except requests.exceptions.RequestException as e:
        st.session_state.auth['error'] = f"An error occurred during logout: {str(e)}"

def login_form():
    """Render the login form and handle submission."""
    with st.form("login_form"):
        st.subheader("Please Add Your Credentials")
        username = st.text_input("👤 Username", key="login_username")
        password = st.text_input("🔑 Password", type="password", key="login_password")

        submitted = st.form_submit_button("Login")

        if submitted:
            if not username or not password:
                st.session_state.auth['error'] = "Please enter both username and password."
            else:
                st.session_state.auth['processing_login'] = True
                st.session_state.auth['login_creds'] = {'username': username, 'password': password}
            st.rerun()

def admin_dashboard():
    """Display the admin dashboard."""
    st.markdown(f"### Welcome Admin, {st.session_state.auth['username']}!")
    
    with st.expander("👤 Add New User"):
        with st.form("add_user_form"):
            new_username = st.text_input("New Username")
            new_password = st.text_input("Password", type="password")
            
            submitted = st.form_submit_button("Create User")
            
            if submitted:
                st.session_state.auth['error'] = None
                st.session_state.auth['success'] = None
                
                if not new_username or not new_password:
                    st.session_state.auth['error'] = "Please enter both username and password."
                    st.rerun()
                
                try:
                    csrf_response = requests.get(
                        urljoin(DJANGO_BASE_URL, "get_csrf/"),
                        cookies=st.session_state.auth['cookies']
                    )
                    csrf_token = csrf_response.cookies.get('csrftoken', '')
                    
                    create_response = requests.post(
                        urljoin(DJANGO_BASE_URL, "create_user/"),
                        data={
                            "username": new_username,
                            "password": new_password,
                            "csrfmiddlewaretoken": csrf_token
                        },
                        cookies=st.session_state.auth['cookies'],
                        headers={
                            "X-CSRFToken": csrf_token,
                            "Referer": DJANGO_BASE_URL
                        },
                        timeout=5
                    )
                    
                    if create_response.status_code == 201:
                        st.session_state.auth['success'] = "User created successfully!"
                    else:
                        error_msg = create_response.json().get('error', 'Unknown error')
                        st.session_state.auth['error'] = f"Error creating user: {error_msg}"
                    
                    st.rerun()
                        
                except Exception as e:
                    st.session_state.auth['error'] = f"Failed to create user: {str(e)}"
                    st.rerun()
    
    # Add the new Delete User section
    with st.expander("🗑️ Delete User"):
        with st.form("delete_user_form"):
            # Get list of users (excluding current admin)
            try:
                users_response = requests.get(
                    urljoin(DJANGO_BASE_URL, "get_users/"),  # You'll need to add this endpoint
                    cookies=st.session_state.auth['cookies'],
                    timeout=5
                )
                users = [u for u in users_response.json() if u != st.session_state.auth['username']]
            except:
                users = []
            
            user_to_delete = st.selectbox("Select User to Delete", users)
            
            submitted = st.form_submit_button("Delete User")
            
            if submitted:
                st.session_state.auth['error'] = None
                st.session_state.auth['success'] = None
                
                try:
                    csrf_response = requests.get(
                        urljoin(DJANGO_BASE_URL, "get_csrf/"),
                        cookies=st.session_state.auth['cookies']
                    )
                    csrf_token = csrf_response.cookies.get('csrftoken', '')
                    
                    delete_response = requests.post(
                        urljoin(DJANGO_BASE_URL, "delete_user/"),
                        data={
                            "username": user_to_delete,
                            "csrfmiddlewaretoken": csrf_token
                        },
                        cookies=st.session_state.auth['cookies'],
                        headers={
                            "X-CSRFToken": csrf_token,
                            "Referer": DJANGO_BASE_URL
                        },
                        timeout=5
                    )
                    
                    if delete_response.status_code == 200:
                        st.session_state.auth['success'] = f"User {user_to_delete} deleted successfully!"
                    else:
                        error_msg = delete_response.json().get('error', 'Unknown error')
                        st.session_state.auth['error'] = f"Error deleting user: {error_msg}"
                    
                    st.rerun()
                        
                except Exception as e:
                    st.session_state.auth['error'] = f"Failed to delete user: {str(e)}"
                    st.rerun()
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.button("Logout", on_click=handle_logout)
    with col2:
        if st.button("🚪 Go to System Main Page"):
            st.switch_page("streamlit_app.py")


# --- Main App Logic ---
st.title("🔒 Authentication System")
st.divider()
# Initialize session state
initialize_session_state()

# Display messages
display_auth_messages()

# Handle login processing
if st.session_state.auth.get('processing_login', False):
    with st.spinner("Authenticating..."):
        creds = st.session_state.auth['login_creds']
        handle_login(creds['username'], creds['password'])
        st.session_state.auth['processing_login'] = False
        st.session_state.auth['login_creds'] = {}
        st.rerun()

# Show appropriate view based on authentication status
if not st.session_state.auth['authenticated']:
    login_form()
else:
    if st.session_state.auth['is_admin']:
        admin_dashboard()
    else:
        st.switch_page("streamlit_app.py")
