import streamlit as st
import asyncio
import pandas as pd
import datetime
import os
import re

# Import modules
from src.database.csv_db import CsvExpenseRepository
from src.services.api_client import ApiClient
from src.services.location_service import LocationService
from src.analytics.charts import ExpenseVisualizer

# --- Page Config ---
st.set_page_config(page_title="Productivity Dashboard", page_icon="🚀", layout="wide")

# --- Initialize Services ---
@st.cache_resource
def get_services():
    csv = 'data/expenses.csv'
    db = CsvExpenseRepository(csv)
    api = ApiClient()
    viz = ExpenseVisualizer(csv)
    loc_service = LocationService()
    
    return db, api, loc_service, viz

db, api, loc_service, viz = get_services()

# --- Async Bridge ---
async def fetch_dashboard_data():
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            city = await loc_service.detect_location(session)
            weather, quote = await api.get_daily_data(city)
            return city, weather, quote
    except Exception:
        return "Colombo", "N/A", "Keep going!"

def load_async_data():
    return asyncio.run(fetch_dashboard_data())

# ==========================================
# 🧠 CATEGORY LOGIC
# ==========================================
def get_unique_categories():
    expenses = db.get_all_expenses()
    default_cats = {"Food", "Transport", "Bills", "Shopping", "Entertainment"}
    
    if expenses:
        existing_cats = {row['Category'].strip().title() for row in expenses}
        all_cats = default_cats.union(existing_cats)
    else:
        all_cats = default_cats
        
    sorted_cats = sorted(list(all_cats))
    return ["➕ Add New Category"] + sorted_cats 

# ==========================================
# 🎨 UI LAYOUT
# ==========================================

st.title("🚀 Personal Productivity Dashboard")
st.markdown("---")

# --- Header ---
with st.spinner('📡 Connecting to satellites...'):
    city, weather, quote = load_async_data()
    col1, col2 = st.columns(2)
    col1.metric("🌤️ Weather", weather.split(',')[0])
    col2.info(f"💡 {quote}")

st.markdown("---")

# ==========================================
# ➕ SIDEBAR: DYNAMIC ADD EXPENSE
# ==========================================
with st.sidebar:
    st.header("➕ Add New Expense")
    
    cat_options = get_unique_categories()
    
    selected_cat = st.selectbox("Select Category", cat_options)
    
    # --- FORM START ---
    with st.form("expense_form", clear_on_submit=True):
        
        final_category = selected_cat
        new_cat_input = None

        if selected_cat == "➕ Add New Category":
            new_cat_input = st.text_input("Enter New Category Name")
        
        amount = st.number_input(
            "Amount (Rs.)", 
            min_value=0.0, 
            step=100.0, 
            value=None, 
            placeholder="Type amount..."
        )
        
        submitted = st.form_submit_button("Save Expense")
        
        if submitted:
            # 1. Check Amount
            if amount is None:
                st.error("⚠️ Please enter an amount.")
                st.stop() 

            # 2. Check Category Logic
            if selected_cat == "➕ Add New Category":
                if not new_cat_input:
                    st.error("⚠️ Please type a name for the new category.")
                    st.stop()
                
                # --- Input VALIDATION LOGIC ---
                if not re.match(r"^[a-zA-Z\s]+$", new_cat_input):
                    st.error("⛔ Invalid Name! Categories cannot contain numbers or special characters (@, $, !, etc). Only letters are allowed.")
                    st.stop()
                
                final_category = new_cat_input.strip().title()
            
            # Save Process
            date = datetime.date.today().isoformat()
            db.add_expense(final_category, amount, date)
            
            # Feedback
            if selected_cat == "➕ Add New Category":
                st.success(f"✅ Created & Saved: **{final_category}**")
            else:
                st.success(f"✅ Saved under **{final_category}**")            
            st.rerun()

# ==========================================
# 📊 MAIN AREA: ANALYTICS
# ==========================================
col_charts, col_data = st.columns([2, 1])
expenses = db.get_all_expenses()

with col_data:
    st.subheader("📋 Recent Expenses")
    if expenses:
        df = pd.DataFrame(expenses)
        st.dataframe(df, use_container_width=True)
        st.metric("💰 Total Spent", f"Rs. {df['Amount'].sum():,.2f}")
    else:
        st.info("No expenses recorded.")

with col_charts:
    st.subheader("📊 Visualizations")
    if expenses:
        tab1, tab2 = st.tabs(["Daily Trend", "Category Pie"])
        with tab1:
            viz.plot_daily_trend()
            if os.path.exists('data/daily_trend.png'):
                st.image('data/daily_trend.png')
        with tab2:
            viz.plot_category_distribution()
            if os.path.exists('data/category_distribution.png'):
                st.image('data/category_distribution.png')
    else:
        st.write("Waiting for data...")