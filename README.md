# 📈 Data Automation Demo: Messy CSV to Clean SQL

This repository demonstrates the process of taking inconsistent, unstructured data from a client-provided CSV file and transforming it into clean, reliable SQL `INSERT` statements ready for direct database ingestion.

### 💡 Problem Solved
Clients often receive data from different sources (marketing tools, legacy systems, external vendors) with inconsistent formatting:
* Mixed date formats (`MM/DD/YY` vs. `DD-MM-YYYY` vs. `YYYY-MM-DD`)
* Non-standard email addresses (`AT` instead of `@`)
* Unnecessary text prefixes in IDs (`ID1234`)
* Inconsistent number formatting.

### ⚙️ The Solution (data_cleaner.py)
This Python script, using the `pandas` library, performs the following cleaning steps:

1.  **Date Standardization:** Converts mixed date formats into a unified `YYYY-MM-DD` standard.
2.  **Email Standardization:** Uses regex to replace non-standard characters (e.g., `AT`) with the standard `@`.
3.  **ID Normalization:** Removes text prefixes (`ID`) and converts the field to a clean integer.
4.  **Price Cleaning:** Ensures all price data is a reliable float (`.00`) format.

### ▶️ Output Example
The script's final output is a series of clean SQL statements ready to be executed:

```sql
INSERT INTO customer_orders (customer_name, customer_email, order_id, total_price, sale_date) VALUES ('ACME, Inc.', 'support@acme.com', '9876', '123.55', '2025-12-14');
INSERT INTO customer_orders (customer_name, customer_email, order_id, total_price, sale_date) VALUES ('Globex CORP', 'globex@corp.org', '5544', '321.00', '2025-10-12');
-- etc.