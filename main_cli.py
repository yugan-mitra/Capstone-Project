import asyncio
import aiohttp
from functools import reduce

# Import our custom modules
from src.database.csv_db import CsvExpenseRepository
from src.services.api_client import ApiClient
from src.analytics.charts import ExpenseVisualizer
from src.services.location_service import LocationService

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
    # 1. Initialize Components
    db = CsvExpenseRepository('data/expenses.csv')
    api = ApiClient()
    viz = ExpenseVisualizer('data/expenses.csv')
    loc_service = LocationService()

    print("\n" + "="*50)
    print("🚀 PRODUCTIVITY DASHBOARD LOADING...")
    print("="*50)

    # 2. Detect Location First (Async)
    print("📡 Detecting Location...")
    async with aiohttp.ClientSession() as session:
        current_city = await loc_service.detect_location(session)
    print(f"📍 Location found: {current_city}")

    # 3. Fetch Data based on location
    print("⏳ Fetching daily briefing...")
    try:
        # Pass the detected city to the API
        weather, quote = await api.get_daily_data(current_city)
        
        print(f"\n🌞 Weather: {weather}")
        print(f"💡 Quote:   {quote}")
    except Exception as e:
        print(f"⚠️ Network Error: {e}")

    print("-" * 50)

    # 4. Interactive Loop
    while True:
        print("\nMain Menu:")
        print("1. ➕ Add Expense")
        print("2. 📊 View Analytics")
        print("3. 🌍 Change Location (Manual)")
        print("4. 🚪 Exit")
        
        choice = input("Select an option (1-4): ")

        if choice == '1':
            pass 

        elif choice == '2':
            pass

        elif choice == '3':
            # Manual Location Logic
            new_city = input("Enter your city name: ")
            loc_service.set_manual_location(new_city)
            
            # Refresh Weather
            print("🔄 Updating Weather...")
            try:
                # We need a quick async call here
                weather, _ = await api.get_daily_data(loc_service.city)
                print(f"✅ Updated: {weather}")
            except Exception as e:
                print("❌ Could not find city.")

        elif choice == '4':
            print("👋 Goodbye!")
            break

if __name__ == "__main__":
    # Start the Async Event Loop
    asyncio.run(main())