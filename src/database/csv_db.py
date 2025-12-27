import csv
import os
from typing import List, Dict
from .repository import ExpenseRepository

class CsvExpenseRepository(ExpenseRepository):
    def __init__(self, filename='data/expenses.csv'):
        self.filename = filename
        self._initialize_file()

    def _initialize_file(self):
        """Creates the CSV file with headers if it doesn't exist."""
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Category', 'Amount', 'Date'])

    def add_expense(self, category: str, amount: float, date: str) -> None:
        """Writes a new row to the CSV file."""
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([category, amount, date])

    def get_all_expenses(self) -> List[Dict]:
        """Reads the CSV and returns data as a list of dictionaries."""
        if not os.path.exists(self.filename):
            return []
            
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            try:
                next(reader)
            except StopIteration:
                return []

            # List Comprehension
            expenses = [
                {'Category': row[0], 'Amount': float(row[1]), 'Date': row[2]} 
                for row in reader if row 
            ]
            return expenses