import sqlite3
import pandas as pd

# 1. Connect to your local database
conn = sqlite3.connect('training_data.db')

# 2. Write the SQL query to grab everything
query = "SELECT * FROM projects"

# 3. Load it directly into a Pandas DataFrame
df = pd.read_sql_query(query, conn)

# 4. Always close the connection to keep the file safe
conn.close()

# --- Verification ---
print(f"Successfully loaded {len(df)} projects into memory!\n")
print(df.head()) # Shows the first 5 rows to prove it works