# Smart Inventory Management System

A modern inventory management system built with Django REST Framework backend and Streamlit frontend, featuring AI-powered assistance through Google's Gemini API.

## Features

- **Product Management**: Add, edit, and track inventory items with units and notes
- **Purchase Tracking**: Record purchases from suppliers with dates and amounts
- **Sales Management**: Track sales to customers with automatic stock validation
- **AI Assistant**: Natural language interface for inventory operations using Gemini AI
- **Real-time Stock Levels**: Automatic calculation of current inventory levels
- **User Authentication**: Secure login system with admin/user roles
- **Filtering & Search**: Advanced filtering for products, purchases, and sales

## Tech Stack

- **Backend**: Django 5.1.6, Django REST Framework
- **Frontend**: Streamlit 1.42.2
- **Database**: SQLite (development), PostgreSQL ready for production
- **AI Integration**: Google Gemini 2.5-flash
- **Authentication**: Django's built-in auth system

## Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Smart_Inventory
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration:
   # - SECRET_KEY (use the provided one or generate new)
   # - GEMINAI_API_KEY (get from Google AI Studio)
   # - DEBUG=False for production
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

## Usage

### Starting the Application

1. **Start Django backend** (Terminal 1):
   ```bash
   python manage.py runserver
   ```

2. **Start Streamlit frontend** (Terminal 2):
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Access the application**:
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000/api/
   - Admin Panel: http://localhost:8000/admin/

### AI Assistant Features

The AI Assistant can handle natural language commands like:
- "Show products"
- "Add a new product named Laptop with unit pieces"
- "Record a purchase of 5 Laptops from SupplierX"
- "Sell 2 laptops to customer1"
- "What's my current stock level for Milk?"

### API Endpoints

- `/api/products/` - Product CRUD operations
- `/api/purchases/` - Purchase management
- `/api/sales/` - Sales tracking
- `/api/check-user-role/` - User role verification
- `/api/create-user/` - User creation (admin only)
- `/api/delete-user/` - User deletion (admin only)

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# API Keys
GEMINAI_API_KEY=your-gemini-api-key-here
```

### Production Deployment

For production deployment:

1. Set `DEBUG=False` in environment variables
2. Configure `ALLOWED_HOSTS` with your domain
3. Use PostgreSQL instead of SQLite
4. Set up proper HTTPS/SSL certificates
5. Configure static file serving
6. Set up monitoring and logging

## Security Features

- Environment variable configuration for sensitive data
- CSRF protection enabled
- Authentication required for API endpoints
- Production security headers (HTTPS, HSTS, XSS protection)
- Input validation and sanitization

## Development

### Running Tests

```bash
python manage.py test
```

### Code Quality

The project includes:
- Proper error handling and logging
- Database query optimization
- Input validation
- Type hints (where applicable)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create an issue in the repository
- Check the documentation
- Review existing issues for solutions

## Project Status

✅ Core functionality complete
✅ AI integration implemented
✅ Security hardening applied
✅ Performance optimizations added
🔄 Continuous improvements in progress