from fastapi import FastAPI, HTTPException
from datetime import date
from backend import db_helper
from typing import List
from pydantic import BaseModel

class Expense(BaseModel):
    expense_date: date
    amount: float
    category: str
    notes: str




app = FastAPI()
@app.get("/expenses/{expense_date}", response_model = List[Expense])    
def get_expenses(expense_date: date):
    try:
        expenses = db_helper.fetch_expenses_for_date(expense_date)
        return expenses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching expenses: {str(e)}")

@app.post("/expenses/{expense_date}")
def add_or_update_expenses(expense_date: date, expenses: List[Expense]):
    try:
        db_helper.delete_expenses_for_date(expense_date)
        for expense in expenses:
            db_helper.insert_expense(expense.expense_date, expense.amount, expense.category, expense.notes)
        return {"message": "Expense added/updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding expense: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

from fastapi import FastAPI
from datetime import date

app = FastAPI()

@app.get("/analytics")
def get_analytics(start_date: date, end_date: date):
    return {
        "total_expenses": 5000,
        "category_breakdown": {
            "Food": 1500,
            "Shopping": 2000,
            "Travel": 1500
        }
    }    