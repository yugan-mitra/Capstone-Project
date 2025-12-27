import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class ExpenseVisualizer:
    def __init__(self, csv_file='data/expenses.csv'):
        self.csv_file = csv_file
        sns.set(style="whitegrid")

    def _load_data(self):
        """Helper to load data safely."""
        if not os.path.exists(self.csv_file):
            print("⚠️ No data found to plot.")
            return None
        return pd.read_csv(self.csv_file)

    def plot_category_distribution(self):
        df = self._load_data()
        if df is None or df.empty: return

        category_sums = df.groupby('Category')['Amount'].sum()

        plt.figure(figsize=(8,8))
        plt.pie(category_sums, labels=category_sums.index.astype(str).tolist(), autopct='%1.1f%%', startangle=140)
        plt.title('Expense Distribution by Category')
        
        # Save graph inside data folder
        plt.savefig('data/category_distribution.png')
        print("✅ Pie chart saved as 'data/category_distribution.png'")
        plt.show()

    def plot_daily_trend(self):
        df = self._load_data()
        if df is None or df.empty: return

        # Ensure Date is datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        plt.figure(figsize=(10,6))
        daily_sums = df.groupby('Date')['Amount'].sum().reset_index()

        sns.lineplot(data=daily_sums, x='Date', y='Amount', marker='o', color='purple')
        plt.title('Daily Expense Trend')
        plt.xlabel('Date')
        plt.ylabel('Total Amount Spent')
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig('data/daily_trend.png')
        print("✅ Line chart saved as 'data/daily_trend.png'")
        plt.show()