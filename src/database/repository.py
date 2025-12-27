from abc import ABC, abstractmethod
from typing import List, Dict

class ExpenseRepository(ABC):
    """
    This is the Interface (Blueprint).
    Any storage system (CSV, SQL, JSON) MUST implement these methods.
    """
    
    @abstractmethod
    def add_expense(self, category: str, amount: float, date: str) -> None:
        """Saves a new expense."""
        pass

    @abstractmethod
    def get_all_expenses(self) -> List[Dict]:
        """Returns a list of all expenses."""
        pass