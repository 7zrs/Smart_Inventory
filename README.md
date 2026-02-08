# 🏢 Smart Inventory Management System

A modern, AI-powered inventory management system that combines the robustness of Django REST Framework with the intuitive interface of Streamlit, enhanced by Google's Gemini 2.5-flash AI for natural language interactions.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [AI Assistant](#ai-assistant)
- [Project Structure](#project-structure)
- [Security](#security)
- [Deployment](#deployment)
- [Credits](#credits)

---

## 🎯 Overview

The Smart Inventory Management System is a comprehensive solution designed for businesses to efficiently manage their product inventory, track purchases and sales, and leverage AI for intelligent data operations. Built with modern web technologies and powered by Google's Gemini AI, this system offers both traditional CRUD operations and natural language processing capabilities.

### What Makes It Smart?

- **AI-Powered Operations**: Interact with your inventory using natural language commands
- **Real-Time Stock Tracking**: Automatic calculation of stock levels based on purchases and sales
- **Intelligent Validation**: Prevents overselling and maintains data integrity
- **Role-Based Access**: Secure admin and user roles with appropriate permissions
- **Modern UI/UX**: Clean, responsive interface built with Streamlit
- **RESTful API**: Complete Django REST Framework backend for extensibility

---

## ✨ Key Features

### 📦 Inventory Management
- Add, edit, and delete products with detailed information
- Track product units (pieces, kg, liters, etc.)
- Add notes for each product
- View real-time stock levels calculated from purchases and sales
- Smart search and filtering capabilities

### 🛒 Purchase Management
- Record purchases from suppliers
- Track purchase dates and amounts
- Automatic stock level updates on purchase
- Prevent duplicate purchase entries
- Filter purchases by product, supplier, or date range

### 💰 Sales Management
- Record sales to customers with validation
- Automatic stock deduction on sale
- Insufficient stock prevention
- Track customer transactions
- Filter sales by product, customer, or date range

### 🤖 AI Assistant
- **Natural Language Processing**: Ask questions in plain English or Arabic
- **Multi-Intent Recognition**: Handles search, add, edit, and delete operations
- **Confirmation System**: Review AI-generated actions before execution
- **Multi-Language Support**: Seamlessly works with bilingual inputs
- **Data Augmentation**: AI has context of current inventory state
- **Batch Operations**: Execute multiple tasks with navigation controls

### 👥 User Management (Admin Only)
- Create new user accounts
- Delete existing users
- View all system users
- Role assignment (admin/regular user)

### 🔐 Authentication & Authorization
- Secure login system with session management
- Password hashing and validation
- Role-based access control (RBAC)
- Admin-only endpoints protection
- CSRF protection enabled
- Session persistence with localStorage

---

## 🛠️ Tech Stack

### Backend
- **Django 5.1.6**: Web framework for building the API
- **Django REST Framework 3.15.2**: RESTful API toolkit
- **SQLite3**: Development database (PostgreSQL-ready for production)
- **Python 3.8+**: Programming language

### Frontend
- **Streamlit 1.42.2**: Interactive web interface
- **Pandas 2.2.3**: Data manipulation and display
- **Plotly**: Interactive visualizations (if needed)

### AI & Machine Learning
- **Google Gemini 2.5-flash**: Natural language processing
- **google-generativeai 0.8.5+**: Python SDK for Gemini API

### Additional Libraries
- **python-dotenv**: Environment variable management
- **requests**: HTTP library for API calls

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit Frontend                    │
│  (streamlit_app.py + pages/*)                          │
│  - UI Components                                        │
│  - Session Management                                   │
│  - Form Dialogs (@st.dialog)                           │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP Requests
                 │ (localhost:8000/api/)
┌────────────────▼────────────────────────────────────────┐
│               Django REST Framework                      │
│  (Smart_Inventory/*, products/*, accounts/*)           │
│  - ViewSets (Product, Purchase, Sale)                  │
│  - Serializers (Validation & Serialization)            │
│  - Authentication (User, Permissions)                   │
└────────────────┬────────────────────────────────────────┘
                 │
         ┌───────┴────────┐
         │                │
┌────────▼──────┐  ┌──────▼─────────┐
│   SQLite DB   │  │  Gemini 2.5    │
│  - Products   │  │    - NLP       │
│  - Purchases  │  │    - Intent    │
│  - Sales      │  │    - Actions   │
│  - Users      │  │                │
└───────────────┘  └────────────────┘
```

### Key Components

1. **Models** (`products/models.py`):
   - `Product`: Master data with calculated stock methods
   - `Purchase`: Incoming inventory transactions
   - `Sale`: Outgoing inventory transactions

2. **Serializers** (`products/serializers.py`):
   - Validation logic
   - Stock availability checks
   - Related field serialization

3. **ViewSets** (`products/views.py`):
   - CRUD operations
   - Authentication enforcement
   - Query filtering

4. **LLM Utilities** (`llm_utilities/utils.py`):
   - Gemini API integration
   - Natural language parsing
   - Task generation and execution

5. **Streamlit Pages** (`pages/*.py`):
   - Inventory.py: Product management
   - Purchases.py: Purchase tracking
   - Sales.py: Sales recording
   - AI_Assistant.py: AI interface
   - Admin.py: User management
   - login.py: Authentication

---

## 📥 Installation

### Prerequisites

- **Python 3.8+** installed
- **pip** package manager
- **Git** (for cloning)
- **Google AI Studio API Key** ([Get one here](https://makersuite.google.com/app/apikey))

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Smart_Inventory
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory:
   ```env
   # Django Settings
   SECRET_KEY=your-django-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Google AI
   GEMINAI_API_KEY=your-gemini-api-key-here

   # Database (optional, defaults to SQLite)
   # DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set username and password.

7. **Load sample data (optional)**
   ```bash
   python manage.py loaddata sample_data.json
   ```

---

## 🚀 Usage

### Starting the Application

You need to run both the Django backend and Streamlit frontend:

#### Option 1: Using the Batch Script (Windows)

Simply double-click `run_project.bat` or run:
```bash
.\run_project.bat
```

This will:
- Check for Python installation
- Activate the virtual environment
- Install/update dependencies
- Run migrations
- Start both Django and Streamlit servers

#### Option 2: Manual Start

**Terminal 1 - Django Backend:**
```bash
python manage.py runserver
```

**Terminal 2 - Streamlit Frontend:**
```bash
streamlit run streamlit_app.py
```

### Accessing the Application

- **Frontend (Main App)**: http://localhost:8501
- **Django API**: http://localhost:8000/api/
- **Django Admin Panel**: http://localhost:8000/admin/

### First Login

1. Navigate to http://localhost:8501
2. Log in with your superuser credentials
3. If you're an admin, you'll see the Admin Dashboard option

---

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/login/` | User login | No |
| POST | `/api/logout/` | User logout | Yes |
| GET | `/api/check-user-role/` | Check user role | Yes |

### Product Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/products/` | List all products | Yes |
| POST | `/api/products/` | Create new product | Yes |
| GET | `/api/products/{id}/` | Get product details | Yes |
| PUT | `/api/products/{id}/` | Update product | Yes |
| DELETE | `/api/products/{id}/` | Delete product | Yes |

### Purchase Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/purchases/` | List all purchases | Yes |
| POST | `/api/purchases/` | Record new purchase | Yes |
| GET | `/api/purchases/{id}/` | Get purchase details | Yes |
| PUT | `/api/purchases/{id}/` | Update purchase | Yes |
| DELETE | `/api/purchases/{id}/` | Delete purchase | Yes |

### Sales Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/sales/` | List all sales | Yes |
| POST | `/api/sales/` | Record new sale | Yes |
| GET | `/api/sales/{id}/` | Get sale details | Yes |
| PUT | `/api/sales/{id}/` | Update sale | Yes |
| DELETE | `/api/sales/{id}/` | Delete sale | Yes |

### Admin Endpoints (Admin Only)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/get_users/` | List all users | Admin |
| POST | `/api/create_user/` | Create new user | Admin |
| POST | `/api/delete_user/` | Delete user | Admin |

### Example API Calls

**Create a Product:**
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=your-session-id" \
  -d '{
    "name": "Laptop",
    "unit": "pieces",
    "notes": "Dell Inspiron 15"
  }'
```

**Record a Sale:**
```bash
curl -X POST http://localhost:8000/api/sales/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=your-session-id" \
  -d '{
    "product": 1,
    "date": "2025-02-08",
    "customer": "John Doe",
    "amount": 2,
    "notes": "Sold via online store"
  }'
```

---

## 🤖 AI Assistant

The AI Assistant uses **Google Gemini 2.5-flash** to understand natural language commands and execute inventory operations.

### How It Works

1. **User Input**: You type a command in natural language (English or Arabic)
2. **Data Augmentation**: System fetches current inventory data and augments your query
3. **Gemini Analysis**: AI analyzes the augmented query and determines intent
4. **Task Generation**: AI generates structured API tasks (search, add, edit, delete)
5. **Confirmation** (if needed): You review and confirm actions before execution
6. **Execution**: System calls appropriate APIs and displays results

### Example Commands

**Search/Query Operations:**
- "Show all products"
- "What's the stock level of Milk?"
- "List purchases from SupplierX"
- "Show sales to CustomerA this week"

**Add Operations:**
- "Add a new product called Laptop with unit pieces"
- "Record a purchase of 50 Milk from DairyFarm"
- "Add a sale of 10 Laptops to TechStore"

**Edit Operations:**
- "Change the unit of Milk to liters"
- "Update the purchase amount to 100"

**Delete Operations:**
- "Delete the product named OldItem"
- "Remove the sale to CustomerX"

### Confirmation System

For write operations (add, edit, delete), the AI Assistant shows:
- **Task details**: What will be done
- **Affected data**: Which records will change
- **Action buttons**:
  - ✅ Confirm This: Execute current task
  - ✅ Confirm All: Execute all tasks
  - ❌ Cancel This: Skip current task
  - ❌ Cancel All: Cancel all tasks
- **Navigation**: First | Prev | Next | Last (for multiple tasks)

---

## 📁 Project Structure

```
Smart_Inventory/
├── Smart_Inventory/           # Django project settings
│   ├── __init__.py
│   ├── settings.py           # Main settings file
│   ├── urls.py               # URL routing
│   └── wsgi.py
│
├── products/                  # Products app
│   ├── migrations/           # Database migrations
│   ├── __init__.py
│   ├── admin.py              # Django admin config
│   ├── models.py             # Product, Purchase, Sale models
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # API viewsets
│   └── urls.py               # API routes
│
├── accounts/                  # User management app
│   ├── migrations/
│   ├── __init__.py
│   ├── views.py              # Auth views
│   └── urls.py
│
├── llm_utilities/            # AI integration
│   ├── __init__.py
│   └── utils.py              # Gemini API logic
│
├── pages/                    # Streamlit pages
│   ├── login.py              # Login page
│   ├── Inventory.py          # Product management
│   ├── Purchases.py          # Purchase tracking
│   ├── Sales.py              # Sales recording
│   ├── AI_Assistant.py       # AI interface
│   └── Admin.py              # User management
│
├── static/                   # Static files (if any)
├── media/                    # Uploaded files (if any)
│
├── streamlit_app.py          # Main Streamlit app (Home)
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example              # Example environment variables
├── .gitignore               # Git ignore rules
├── run_project.bat          # Windows startup script
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose config
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key | - | Yes |
| `DEBUG` | Debug mode | `False` | No |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` | No |
| `GEMINAI_API_KEY` | Google Gemini API key | - | Yes |
| `DATABASE_URL` | Database connection URL | SQLite | No |

### Django Settings

Key settings in `Smart_Inventory/settings.py`:

```python
# CORS (if needed for external frontend)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8501",
]

# Session Configuration
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  # Set True in production with HTTPS
SESSION_COOKIE_SAMESITE = 'Lax'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### Streamlit Configuration

Create `.streamlit/config.toml`:

```toml
[server]
port = 8501
headless = true

[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

---

## 🔒 Security

### Implemented Security Measures

1. **Authentication & Authorization**
   - Session-based authentication
   - Password hashing with Django's built-in system
   - Role-based access control (RBAC)
   - Admin-only endpoint protection

2. **CSRF Protection**
   - Django CSRF middleware enabled
   - CSRF tokens in forms

3. **Input Validation**
   - DRF serializer validation
   - Model-level validation with `clean()` methods
   - SQL injection prevention via ORM

4. **Data Integrity**
   - Foreign key constraints
   - Unique constraints (unique_together)
   - Stock validation (prevent negative stock)

5. **Production Security Headers** (when DEBUG=False)
   - HTTPS enforcement
   - HSTS (HTTP Strict Transport Security)
   - XSS protection
   - Content type nosniff


---


## 🚢 Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL database
- [ ] Set strong `SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Configure static file serving
- [ ] Set up logging and monitoring
- [ ] Configure backup strategy
- [ ] Implement rate limiting
- [ ] Set up CI/CD pipeline

### Deployment Options

#### Option 1: Traditional Server (VPS)

1. **Set up server** (Ubuntu, CentOS, etc.)
2. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip postgresql nginx
   ```
3. **Clone repository and configure**
4. **Set up Gunicorn** for Django:
   ```bash
   pip install gunicorn
   gunicorn Smart_Inventory.wsgi:application --bind 0.0.0.0:8000
   ```
5. **Configure Nginx** as reverse proxy
6. **Set up Supervisor** for process management
7. **Deploy Streamlit** on separate port (e.g., 8501)

#### Option 2: Docker

1. **Build the image**:
   ```bash
   docker build -t smart-inventory .
   ```
2. **Run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

#### Option 3: Cloud Platforms

**Heroku:**
- Django: Deploy as web dyno
- Streamlit: Deploy as separate app
- Database: Heroku Postgres add-on

**AWS:**
- Django: Elastic Beanstalk or ECS
- Streamlit: EC2 or ECS
- Database: RDS PostgreSQL

**Render:**
- Django: Web Service
- Streamlit: Web Service
- Database: Managed PostgreSQL

**Railway:**
- One-click deployment for both services


---

## 👥 Credits

### Development Team

This project was developed as part of the **BPR601** course at **Syrian Virtual University (SVU)**.

**Developers:**
- **Hasan Zidan** - Frontend Development (Streamlit, UI/UX, Session Management)
  - Student ID: `hasan_171117`
  - Contributions: Streamlit pages, dialog popups, session state management, UI design, Security

- **Ali Al_Ali** - Backend Development (Django, APIs, AI Integration)
  - Student ID: `ali_171119`
  - Contributions: Django models, REST API, Gemini AI integration, database design

---
