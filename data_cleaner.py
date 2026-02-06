import pandas as pd
import re # We'll use this for email cleaning

# --- 1. Define the Cleaning/Transformation Logic ---

# Define the target table and columns for the SQL INSERT statement
TARGET_TABLE = "customer_orders"
TARGET_COLUMNS = ["customer_name", "customer_email", "order_id", "total_price", "sale_date"]

def generate_insert_statement(row):
    """Formats a cleaned DataFrame row into a clean SQL INSERT statement."""
    
    # Simple formatting and quoting for SQL values
    # Note: We use f-strings for clean concatenation
    values = (
        f"'{row['customer_name']}'",
        f"'{row['customer_email']}'",
        f"'{row['order_id']}'",
        f"{row['total_price']}",
        f"'{row['sale_date']}'"
    )

    # Put the final statement together
    sql = f"INSERT INTO {TARGET_TABLE} ({', '.join(TARGET_COLUMNS)}) VALUES ({', '.join(values)});"
    return sql


# --- 2. Main Cleaning Process ---

try:
    # Read the messy CSV file
    df = pd.read_csv('messy_data.csv')
    
    print("--- 1. Input Data (messy_data.csv) ---")
    print(df.head().to_markdown(index=False))
    print("\n" + "="*50 + "\n")

    # --- Data Cleaning Steps using pandas ---

    # 1. Standardize Column Names (optional but professional)
    df.columns = df.columns.str.lower().str.replace('[^a-zA-Z0-9_]', '', regex=True)
    
    # 2. Clean Email: Replace ' AT ' with '@'
    df['email'] = df['email'].str.replace(' AT ', '@', regex=False)
    
    # 3. Clean Order ID: Remove 'ID' prefix and convert to integer
    df['order_id'] = df['order_id'].astype(str).str.replace('ID', '', regex=False).astype(int)

    # 4. Clean Total Price: Ensure it's a clean float 
    df['total_price'] = df['total_price'].astype(str).str.replace('"', '', regex=False).astype(float).round(2)
    
    # 5. Standardize Date Format: Inferring mixed formats and converting to YYYY-MM-DD
    df['date_of_sale'] = pd.to_datetime(df['date_of_sale'], dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d')

    # 6. Rename Final Columns to match our target SQL structure
    df_cleaned = df.rename(columns={
        'client_name': 'customer_name',
        'email': 'customer_email',
        'date_of_sale': 'sale_date'
    })

    # Ensure we only keep the columns we want for the SQL insert, in the right order
    df_cleaned = df_cleaned[TARGET_COLUMNS]

    print("--- 2. Cleaned Data (pandas DataFrame) ---")
    print(df_cleaned.to_markdown(index=False))
    print("\n" + "="*50 + "\n")

    # --- 3. Generate SQL Output ---
    
    print("--- 3. Final SQL Output (Ready for Database Insert) ---")
    # Apply the function to each row to generate the INSERT statement
    df_cleaned['sql_statement'] = df_cleaned.apply(generate_insert_statement, axis=1)

    for statement in df_cleaned['sql_statement']:
        print(statement)
        
except FileNotFoundError:
    print("Error: 'messy_data.csv' not found. Please ensure the file is in the same directory.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")