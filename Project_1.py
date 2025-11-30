import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

plt.style.use('seaborn-v0_8-darkgrid')

def run_sales_analysis(file_path):
    """
    Loads sales data, performs time series and categorical analysis,
    generates line, bar, and pie charts, and saves them to PNG files.
    
    Args:
        file_path (str): The path to the CSV data file.
    """
# 1. Load and Prepare Data
    try:
        df = pd.read_csv("amazon_sales_2025_INR.csv")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    
    # Convert 'Date' to datetime objects
    df['Date'] = pd.to_datetime(df['Date'])
    
    df['Total_Sales_INR'] = pd.to_numeric(df['Total_Sales_INR'], errors='coerce')
    
    # Drop any rows where sales could not be converted (if any)
    df.dropna(subset=['Total_Sales_INR'], inplace=True)
    
    # Set 'Date' as index for time series analysis
    df.set_index('Date', inplace=True)

# 2. Time Series Aggregation
    
    # Daily sales are the base for the most granular line chart
    daily_sales = df['Total_Sales_INR'].resample('D').sum()
    
    # Monthly aggregation
    monthly_sales = df['Total_Sales_INR'].resample('M').sum()
    
    # Quarterly aggregation
    quarterly_sales = df['Total_Sales_INR'].resample('Q').sum()

# 3. Plotting Sales Over Time (Line Charts)
    
    # Define a custom formatter to display large numbers cleanly on the Y-axis
    def format_y_axis(ax):
        """Formats the Y-axis to prevent scientific notation."""
        ax.ticklabel_format(style='plain', axis='y')
        ax.get_yaxis().set_major_formatter(
            plt.FuncFormatter(lambda x, p: f'{x:,.0f}')
        )

    # Daily Sales Line Chart (Most granular view)
    plt.figure(figsize=(14, 6))
    daily_sales.plot(kind='line', color='#1f77b4', linewidth=1)
    plt.title('Daily Total Sales (INR) Over Time', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Total Sales (INR)', fontsize=12)
    plt.legend(['Daily Sales'], loc='upper left')
    plt.xticks(rotation=45, ha='right')
    format_y_axis(plt.gca())
    plt.tight_layout()
    plt.savefig('daily_sales_line_chart.png')
    plt.close()
    print("Chart saved: daily_sales_line_chart.png")

    # Monthly Sales Line Chart (Aggregation)
    plt.figure(figsize=(10, 5))
    # Format index for better readability on x-axis
    monthly_sales.index = monthly_sales.index.strftime('%Y-%m')
    monthly_sales.plot(kind='line', marker='o', color='#2ca02c', linewidth=2)
    plt.title('Monthly Total Sales (INR)', fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Sales (INR)', fontsize=12)
    plt.legend(['Monthly Sales'], loc='upper left')
    plt.xticks(rotation=45, ha='right')
    format_y_axis(plt.gca())
    plt.tight_layout()
    plt.savefig('monthly_sales_line_chart.png')
    plt.close()
    print("Chart saved: monthly_sales_line_chart.png")

    # Quarterly Sales Line Chart (Aggregation)
    plt.figure(figsize=(8, 5))
    # Format index for better readability on x-axis (e.g., 2025Q1)
    quarterly_sales.index = quarterly_sales.index.to_period('Q').astype(str) 
    quarterly_sales.plot(kind='line', marker='s', color='#ff7f0e', linewidth=3)
    plt.title('Quarterly Total Sales (INR)', fontsize=16, fontweight='bold')
    plt.xlabel('Quarter', fontsize=12)
    plt.ylabel('Total Sales (INR)', fontsize=12)
    plt.legend(['Quarterly Sales'], loc='upper left')
    plt.xticks(rotation=0)
    format_y_axis(plt.gca())
    plt.tight_layout()
    plt.savefig('quarterly_sales_line_chart.png')
    plt.close()
    print("Chart saved: quarterly_sales_line_chart.png")

# 4. Categorical Analysis

    # Calculate total sales by product category
    category_sales = df.groupby('Product_Category')['Total_Sales_INR'].sum().sort_values(ascending=False)
    
    # Calculate percentage share
    category_share = (category_sales / category_sales.sum()) * 100

# 5. Plotting Categorical Data (Bar and Pie Charts)

    # Sales by Category Bar Chart (Comparison)
    plt.figure(figsize=(10, 6))
    bars = plt.bar(category_sales.index, category_sales.values, color='#d62728')
    plt.title('Total Sales (INR) by Product Category', fontsize=16, fontweight='bold')
    plt.xlabel('Product Category', fontsize=12)
    plt.ylabel('Total Sales (INR)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    format_y_axis(plt.gca())
    
    # Add data labels for clarity
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + (yval * 0.01), 
                 f'{yval:,.0f}', ha='center', va='bottom', fontsize=9)
                 
    plt.tight_layout()
    plt.savefig('category_sales_bar_chart.png')
    plt.close()
    print("Chart saved: category_sales_bar_chart.png")


    # Sales Share by Category Pie Chart
    plt.figure(figsize=(9, 9))
    plt.pie(
        category_share,
        labels=category_share.index,
        autopct='%1.1f%%',         # Format for percentages
        startangle=90,             # Start the largest slice at the top
        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5},
        textprops={'fontsize': 10}
    )
    plt.title('Total Sales Share by Product Category', fontsize=16, fontweight='bold')
    plt.ylabel('') # Hide the default y-label for pie charts
    plt.tight_layout()
    plt.savefig('category_sales_pie_chart.png')
    plt.close()
    print("Chart saved: category_sales_pie_chart.png")

# Execution
if __name__ == "__main__":
    data_file = 'amazon_sales_2025_INR.csv'
    run_sales_analysis(data_file)
    print("\n All charts have been generated and saved as PNG files in the current directory.")
    print("Review the 'analysis_summary.md' file for the discussion and findings.")