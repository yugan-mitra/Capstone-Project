import asyncio
import aiohttp
import datetime
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
    if high_expenses:
        print(f"\n💸 High Expenses (> 5000): {len(high_expenses)} found")

    # 2. Map: Extract Amounts
    amounts = list(map(lambda x: x['Amount'], expenses))

    # 3. Reduce: Total Calculation
    if amounts:
        total = reduce(lambda a, b: a + b, amounts)
        print(f"💰 Total Spent: Rs. {total:.2f}")
        print(f"📉 Average Transaction: Rs. {total/len(expenses):.2f}")

# --- Main Async Function ---
async def main():
    # 1. Initialize Components
    csv = 'data/expenses.csv'
    db = CsvExpenseRepository(csv)
    api = ApiClient()
    viz = ExpenseVisualizer(csv)
    loc_service = LocationService()

    print("\n" + "="*50)
    print("🚀 PRODUCTIVITY DASHBOARD LOADING...")
    print("="*50)

    # 2. Detect Location First (Async)
    print("📡 Detecting Location...")
    try:
        async with aiohttp.ClientSession() as session:
            current_city = await loc_service.detect_location(session)
        print(f"📍 Location found: {current_city}")
    except Exception as e:
        current_city = "Colombo" # Fallback
        print(f"⚠️ Location Detect Failed: {e}. Defaulting to Colombo.")

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
            # --- [COMPLETE] Add Expense Logic ---
            print("\n--- Add New Expense ---")
            category = input("Enter Category (e.g., Food, Travel): ")
            try:
                amount = float(input("Enter Amount: "))
                date = datetime.date.today().isoformat()
                
                db.add_expense(category, amount, date)
                print("✅ Expense added successfully!")
            except ValueError:
                print("❌ Invalid amount. Please enter a numeric value.")

        elif choice == '2':
            # --- [COMPLETE] View Analytics Logic ---
            print("\n--- Generating Analytics ---")
            
            # 1. Generate Charts
            print("📊 Generating charts (Check 'data' folder)...")
            viz.plot_category_distribution()
            viz.plot_daily_trend()
            
            # 2. Show Text Summary
            print("\n--- Data Summary ---")
            data = db.get_all_expenses()
            print_summary(data)

        elif choice == '3':
            # Manual Location Logic
            new_city = input("\nEnter your city name: ")
            loc_service.set_manual_location(new_city)
            
            # Refresh Weather for new location
            print("🔄 Updating Weather...")
            try:
                # We reuse the API client to fetch data for the new city
                weather, _ = await api.get_daily_data(loc_service.city)
                print(f"✅ Updated Weather: {weather}")
            except Exception as e:
                print(f"❌ Could not update weather: {e}")

        elif choice == '4':
            print("👋 Goodbye! Stay Productive.")
            break
        
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    # Start the Async Event Loop
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🚫 App stopped by user.")