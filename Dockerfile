# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Ensure Streamlit listens on all interfaces
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose ports for Django and Streamlit
EXPOSE 8000
EXPOSE 8501

# Run manage.py runserver when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
