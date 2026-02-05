# Smart Inventory System

A smart inventory management system built with **Django** (Backend) and **Streamlit** (Frontend), featuring AI-powered interactions using **Google Gen AI**.

## 🚀 Quick Start

### Option 1: Run with Docker (Recommended)
This is the easiest way to run the application. It creates a containerized environment with all dependencies.

1.  **Run the script**:
    Double-click `run_docker.bat` or run in terminal:
    ```powershell
    .\run_docker.bat
    ```
    *This will build the image, start the containers, and open the Streamlit app in your browser.*

2.  **Access**:
    *   **Frontend (Streamlit)**: [http://localhost:8501](http://localhost:8501)
    *   **Backend (Django)**: [http://localhost:8000](http://localhost:8000)

3.  **Stop**: Press `Ctrl+C` in the terminal.

---

### Option 2: Run Locally (Windows)
If you prefer running directly on your machine:

1.  **Run the script**:
    Double-click `run_project.bat` or run in terminal:
    ```powershell
    .\run_project.bat
    ```
    *This will check for Python, set up the virtual environment, install requirements, and start the server.*

## 🛠️ Tech Stack
*   **Backend**: Django 5.1
*   **Frontend**: Streamlit
*   **Database**: SQLite (Default)
*   **AI**: Google Gen AI (Gemini 2.0 Flash)

## 📂 Project Structure
*   `manage.py`: Django entry point (also launches Streamlit).
*   `streamlit_app.py`: Main Streamlit application entry.
*   `pages/`: Streamlit pages (Login, etc.).
*   `llm_utilities/`: AI integration logic.
