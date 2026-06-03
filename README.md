# Expense Tracking System

A full-stack web application for tracking and analyzing personal expenses. Built with FastAPI for the backend API, Streamlit for the frontend, and MySQL for data persistence.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Database Schema](#database-schema)
- [Usage Guide](#usage-guide)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- **Add Expenses**: Record daily expenses with date, amount, category, and notes
- **View Expenses**: Retrieve and display expenses for a specific date
- **Update Expenses**: Modify or replace expenses for a given date
- **Delete Expenses**: Remove expenses from the database
- **Analytics Dashboard**: View expense analytics and summaries over date ranges
- **Category Tracking**: Organize expenses by categories (Food, Shopping, Transportation, Entertainment, Utilities, Other)
- **Real-time UI**: Interactive web interface built with Streamlit
- **RESTful API**: FastAPI backend with comprehensive error handling

## 📁 Project Structure

```
Project_Expense_tracking_sys/
├── backend/
│   ├── __init__.py
│   ├── server.py                 # FastAPI server and route definitions
│   ├── db_helper.py              # Database utility functions
│   └── logging_setup.py           # Logging configuration
├── Frontend/
│   └── (currently empty)          # Reserved for additional frontend files
├── test/
│   ├── conftest.py               # Pytest configuration
│   ├── backend/
│   │   ├── db_helper.py          # Database helper mock/fixture
│   │   └── test_db_helper.py     # Database tests
│   └── Frontend/
│       └── app.py                # Streamlit frontend app
├── test_db_connection.py         # Database connection validation script
└── server.log                    # Application logs
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern async web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI
- **Pydantic** - Data validation and serialization
- **MySQL** - Relational database
- **mysql-connector-python** - MySQL database driver

### Frontend
- **Streamlit** - Rapid web app development framework
- **Pandas** - Data manipulation and analysis
- **Requests** - HTTP client for API communication

### Testing & Development
- **Pytest** - Testing framework
- **Python 3.14.3** - Programming language

## 📦 Prerequisites

- Python 3.11+ (tested on 3.14.3)
- MySQL Server running locally
- MySQL database named `expense_manager` with credentials (root/root)

## 🚀 Installation

### 1. Clone or Setup the Project

```bash
cd Project_Expense_tracking_sys
```

### 2. Install Dependencies

Install all required Python packages:

```bash
python -m pip install -r requirements.txt
```

Or install packages individually:

```bash
python -m pip install fastapi uvicorn pydantic mysql-connector-python streamlit pandas requests
```

### 3. Set Up MySQL Database

Create the database and expenses table:

```sql
CREATE DATABASE IF NOT EXISTS expense_manager;

USE expense_manager;

CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expense_date DATE NOT NULL,
    amount FLOAT NOT NULL,
    category VARCHAR(50) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Verify Database Connection

Test your MySQL connection:

```bash
python test_db_connection.py
```

You should see output showing the database structure and any existing expenses.

## ⚙️ Configuration

### Database Configuration

Edit `backend/db_helper.py` to update database credentials if needed:

```python
connection = mysql.connector.connect(
    host="localhost",      # Change if MySQL is on different host
    user="root",           # Update username
    password="root",       # Update password
    database="expense_manager"  # Database name
)
```

### API Server Configuration

In `backend/server.py`, you can modify the server settings:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
```

## 🎯 Running the Application

### Option 1: Run Both Backend and Frontend (Recommended)

#### Terminal 1 - Start the Backend API

```bash
python -m uvicorn backend.server:app --reload --host localhost --port 8000
```

Or simply:

```bash
python backend/server.py
```

Expected output:
```
Uvicorn running on http://localhost:8000
```

#### Terminal 2 - Start the Frontend

```bash
python -m streamlit run test/Frontend/app.py
```

Expected output:
```
Uvicorn server started on 0.0.0.0:8501
Local URL: http://localhost:8501
```

### Option 2: Just Run the API

```bash
python backend/server.py
```

Then use a tool like `curl`, Postman, or the provided API endpoints.

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Get Expenses for a Date
**GET** `/expenses/{expense_date}`

Retrieve all expenses for a specific date.

- **Parameters:**
  - `expense_date` (path): Date in `YYYY-MM-DD` format

- **Response (200):**
```json
[
  {
    "expense_date": "2024-08-01",
    "amount": 500.0,
    "category": "Food",
    "notes": "Grocery shopping"
  }
]
```

- **Example:**
```bash
curl http://localhost:8000/expenses/2024-08-01
```

#### 2. Add or Update Expenses
**POST** `/expenses/{expense_date}`

Add new expenses or replace existing ones for a date.

- **Parameters:**
  - `expense_date` (path): Date in `YYYY-MM-DD` format
  - `expenses` (body): Array of expense objects

- **Request Body:**
```json
[
  {
    "expense_date": "2024-08-01",
    "amount": 250.50,
    "category": "Food",
    "notes": "Lunch at restaurant"
  }
]
```

- **Response (200):**
```json
{
  "message": "Expense added/updated successfully"
}
```

- **Example:**
```bash
curl -X POST http://localhost:8000/expenses/2024-08-01 \
  -H "Content-Type: application/json" \
  -d '[{"expense_date": "2024-08-01", "amount": 250.50, "category": "Food", "notes": "Lunch"}]'
```

#### 3. Get Analytics
**GET** `/analytics`

Retrieve expense analytics for a date range.

- **Parameters:**
  - `start_date` (query): Start date in `YYYY-MM-DD` format
  - `end_date` (query): End date in `YYYY-MM-DD` format

- **Response (200):**
```json
{
  "total_expenses": 5000,
  "category_breakdown": {
    "Food": 1500,
    "Transportation": 1200,
    "Shopping": 2300
  }
}
```

- **Example:**
```bash
curl "http://localhost:8000/analytics?start_date=2024-08-01&end_date=2024-08-31"
```

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Run specific test file:

```bash
pytest test/backend/test_db_helper.py
```

Run tests with coverage:

```bash
pytest --cov=backend
```

## 🗄️ Database Schema

### expenses table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique expense ID |
| expense_date | DATE | NOT NULL | Date of the expense |
| amount | FLOAT | NOT NULL | Expense amount in currency units |
| category | VARCHAR(50) | NOT NULL | Category of expense |
| notes | TEXT | NULL | Optional notes about the expense |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

## 💡 Usage Guide

### Using the Streamlit Frontend

1. Open your browser to `http://localhost:8501`

2. **Add Expense Tab:**
   - Select a date using the date picker
   - Enter the amount (>0)
   - Choose a category from dropdown
   - Add optional notes
   - Click "Add Expense"

3. **View Expenses Tab:**
   - Automatically shows expenses for the date you selected
   - Displays in a table format with all expense details

4. **Analytics Tab:**
   - Select start and end dates
   - Click "Generate Analytics"
   - View total expenses and category breakdown

### Using the API Directly

Example workflow:

```bash
# Add expense
curl -X POST http://localhost:8000/expenses/2024-08-01 \
  -H "Content-Type: application/json" \
  -d '[{
    "expense_date": "2024-08-01",
    "amount": 100,
    "category": "Food",
    "notes": "Coffee"
  }]'

# Get expenses
curl http://localhost:8000/expenses/2024-08-01

# Get analytics
curl "http://localhost:8000/analytics?start_date=2024-08-01&end_date=2024-08-31"
```

## 🐛 Troubleshooting

### Issue: "Cannot connect to backend server at localhost:8000"

**Solution:**
- Make sure the backend is running: `python backend/server.py`
- Check if port 8000 is available
- Verify firewall isn't blocking connections

### Issue: "ImportError: cannot import name 'DEFAULT_EXCLUDED_CONTENT_TYPES'"

**Solution:**
- This is a starlette/streamlit compatibility issue
- The project includes a patched version of streamlit middleware
- If you encounter this, reinstall streamlit: `pip install --upgrade streamlit`

### Issue: "mysql.connector.errors.ProgrammingError: Unknown database"

**Solution:**
- Create the `expense_manager` database in MySQL:
  ```sql
  CREATE DATABASE expense_manager;
  ```
- Or run `test_db_connection.py` to verify setup

### Issue: "Access denied for user 'root'@'localhost'"

**Solution:**
- Update database credentials in `backend/db_helper.py`
- Or verify MySQL root password is "root"
- Check MySQL service is running

### Issue: Streamlit not starting

**Solution:**
```bash
# Reinstall streamlit
pip install --upgrade streamlit starlette

# Try running again
python -m streamlit run test/Frontend/app.py
```

## 📝 Logging

Application logs are written to `server.log`. Each log entry includes:
- Timestamp
- Logger name
- Log level (INFO, ERROR, etc.)
- Message

Example:
```
2024-08-01 10:30:45,123 - db_helper - INFO - fetch_expenses_for_date called with 2024-08-01
```

## 🔒 Security Notes

- Currently uses hardcoded credentials (root/root) - update for production
- No authentication implemented - add user authentication for production
- Input validation via Pydantic models
- SQL injection protection via parameterized queries

## 🚀 Future Enhancements

- [ ] User authentication and authorization
- [ ] Budget planning and alerts
- [ ] Expense export (CSV, PDF)
- [ ] Data visualization (charts, graphs)
- [ ] Recurring expenses
- [ ] Multi-user support
- [ ] API rate limiting
- [ ] Advanced filtering and search

## 📄 License

This project is provided as-is for educational purposes.

## 👨‍💻 Contributing

To contribute to this project:

1. Create a feature branch
2. Make your changes
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

---

**Last Updated:** June 2, 2026  
**Version:** 1.0.0
