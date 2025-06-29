import streamlit as st
import requests
import json
from urllib.parse import urljoin

# Configuration
DJANGO_BASE_URL = "http://127.0.0.1:8000/"
LOGIN_URL = urljoin(DJANGO_BASE_URL, "login/")
LOGOUT_URL = urljoin(DJANGO_BASE_URL, "logout/")

def initialize_session_state():
    """Initialize all session state variables for authentication."""
    if 'auth' not in st.session_state:
        st.session_state.auth = {
            'authenticated': False,
            'username': None,
            'error': None,
            'success': None,
            'processing_login': False, # Flag to indicate a login attempt is in progress
            'login_creds': {}          # To temporarily store credentials
        }

def display_auth_messages():
    """Display authentication success/error messages and clear them."""
    if st.session_state.auth.get('error'):
        st.error(st.session_state.auth['error'])
        st.session_state.auth['error'] = None # Clear after displaying

    if st.session_state.auth.get('success'):
        st.success(st.session_state.auth['success'])
        st.session_state.auth['success'] = None # Clear after displaying

def handle_login(username, password):
    """Handle the login process with the Django backend."""
    st.session_state.auth['error'] = None # Clear previous errors
    st.session_state.auth['success'] = None # Clear previous success messages

    try:
        # Sending data as form-encoded, which Django's request.POST expects by default
        response = requests.post(
            LOGIN_URL,
            data={'username': username, 'password': password},
            timeout=5 # Set a timeout for the request
        )

        # Check if the response content type is JSON before attempting to parse
        if 'application/json' in response.headers.get('Content-Type', ''):
            response_data = response.json()
        else:
            # If not JSON, it might be an HTML error page or empty response
            st.session_state.auth['error'] = f"Unexpected response from server (Status: {response.status_code}). Raw: {response.text[:200]}..."
            return

        if response.status_code == 200:
            # Assuming Django sends back a JSON response with 'message' and possibly 'status'
            if response_data.get('status') == 'success':
                st.session_state.auth.update({
                    'authenticated': True,
                    'username': username,
                    'success': response_data.get('message', 'Login successful!')
                })
            else:
                st.session_state.auth['error'] = response_data.get('message', 'Login failed: Invalid credentials.')
        else:
            # Handle other HTTP status codes (e.g., 400 Bad Request, 403 Forbidden)
            st.session_state.auth['error'] = response_data.get('message', f"Login failed with status code: {response.status_code}")

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
    st.session_state.auth['error'] = None # Clear previous errors
    st.session_state.auth['success'] = None # Clear previous success messages

    try:
        # A GET request for logout is common, but a POST can be more secure
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
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        submitted = st.form_submit_button("Login")

        if submitted:
            if not username or not password:
                st.session_state.auth['error'] = "Please enter both username and password."
            else:
                # Set flag and store credentials to handle the login on the next script run
                st.session_state.auth['processing_login'] = True
                st.session_state.auth['login_creds'] = {'username': username, 'password': password}
            # Rerun immediately to either show the missing fields error or to start processing the login
            st.rerun()


# --- Main App Logic ---

st.title("Streamlit Authentication System")

# Ensure all state variables are initialized
initialize_session_state()

# Always display messages at the top
display_auth_messages()

# If a login is in progress, show spinner and handle authentication
if st.session_state.auth.get('processing_login', False):
    with st.spinner("Authenticating..."):
        creds = st.session_state.auth['login_creds']
        handle_login(creds['username'], creds['password'])
        
        # Reset the processing flag and credentials after the attempt
        st.session_state.auth['processing_login'] = False
        st.session_state.auth['login_creds'] = {}
        
        # Rerun to show the outcome (logged in, or form with an error)
        st.rerun()

# If not authenticated and not processing, show the login form
elif not st.session_state.auth['authenticated']:
    login_form()

# If authenticated, show the main content
else:
    st.markdown(f"### Welcome, {st.session_state.auth['username']}!")
    st.write("You are successfully logged in and can now access protected content.")

    st.markdown("---") # Separator for logged-in content
    st.subheader("Protected Content")
    st.write("This is some content only visible when authenticated.")
    if st.button("Logout"):
        handle_logout()
        st.rerun() # Rerun to show login form after logout
