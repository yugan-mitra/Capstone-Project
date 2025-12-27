import asyncio
import datetime
import os
from functools import reduce

# Import our custom modules
from src.database.csv_db import CsvExpenseRepository
from src.services.api_client import ApiClient
from src.analytics.charts import ExpenseVisualizer

# --- Helper Function for Analysis ---
def print_summary(expenses):
    if not expenses:
        print("📭 No expenses recorded yet.")
        return

    # 1. Filter: High Expenses (> 5000)
    high_expenses = list(filter(lambda x: x['Amount'] > 5000, expenses))
    print(f"\n💸 High Expenses (> 5000): {len(high_expenses)} found")

    # 2. Map: Extract Amounts
    amounts = list(map(lambda x: x['Amount'], expenses))

    # 3. Reduce: Total Calculation
    total = reduce(lambda a, b: a + b, amounts)
    
    print(f"💰 Total Spent: Rs. {total:.2f}")
    print(f"📉 Average Transaction: Rs. {total/len(expenses):.2f}")

# --- Main Async Function ---
async def main():
    # 1. Initialize Components (OOP)
    db = CsvExpenseRepository('data/expenses.csv')
    api = ApiClient()
    viz = ExpenseVisualizer('data/expenses.csv')

    print("\n" + "="*50)
    print("🚀 PRODUCTIVITY DASHBOARD LOADING...")
    print("="*50)

    # 2. Fetch Live Data (Asynchronous)
    print("⏳ Fetching daily briefing (Weather & Quotes)...")
    try:
        # This runs in parallel!
        weather, quote = await api.get_daily_data()
        
        print(f"\n🌞 Weather: {weather}")
        print(f"💡 Quote:   {quote}")
    except Exception as e:
        print(f"⚠️ Network Error: {e}")

    print("-" * 50)

    # 3. Interactive Loop
    while True:
        print("\nMain Menu:")
        print("1. ➕ Add Expense")
        print("2. 📊 View Analytics (Charts)")
        print("3. 📋 View Summary (Data)")
        print("4. 🚪 Exit")
        
        choice = input("Select an option (1-4): ")

        if choice == '1':
            cat = input("Enter Category (Food/Transport/Bills): ")
            try:
                amt = float(input("Enter Amount: "))
                date = datetime.date.today().isoformat()
                
                # Save using OOP Interface
                db.add_expense(cat, amt, date)
                print("✅ Expense Saved!")
            except ValueError:
                print("❌ Invalid amount.")

        elif choice == '2':
            print("generating charts...")
            viz.plot_category_distribution()
            viz.plot_daily_trend()

        elif choice == '3':
            # Get data from DB and analyze
            data = db.get_all_expenses()
            print_summary(data)

        elif choice == '4':
            print("👋 Goodbye! Stay Productive.")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    # Start the Async Event Loop
    asyncio.run(main())