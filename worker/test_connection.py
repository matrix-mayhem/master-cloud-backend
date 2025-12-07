# test_connection.py (Place this in your project root or worker/ folder)

import os
import sys
from sqlalchemy.sql import text
import yfinance as yf
import pandas as pd
import sys

# --- Verify PYTHONPATH and Module Imports ---
print("--- 1. Python Path Check ---")
# This confirms '/app' is in the search path, which is necessary for 'backend' imports.
if "/app" not in sys.path:
    print("WARNING: /app is not in sys.path. Imports might fail.")
else:
    print("SUCCESS: /app is in sys.path.")

print("\n--- 2. Module Import Check ---")
try:
    # Attempt to import a module from your worker code
    from worker.tasks.finance.ingest import ingest_ohlc
    # Attempt to import the shared model
    from backend.app.models.candle import Candle
    print("SUCCESS: Internal modules (worker and backend) imported.")
except ImportError as e:
    print(f"FAILURE: Module import failed. Error: {e}")
    sys.exit(1)

# --- Database/Redis Connection Checks ---

# 3. Redis Connection Check (using environment variables from docker-compose.yml)
print("\n--- 3. Redis Connection Check ---")
import redis
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379)) 

try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=False)
    r.ping()
    print(f"SUCCESS: Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
except redis.exceptions.ConnectionError as e:
    print(f"FAILURE: Could not connect to Redis. Check the 'redis' service. Error: {e}")
    
# 4. PostgreSQL Connection Check (requires your database setup code)
print("\n--- 4. PostgreSQL Connection Check ---")
try:
    # Assuming your database connection setup is in a file like backend/app/database/finance_db.py
    # You'll need to use the absolute import path here.
    from backend.app.database.finance_db import engine
    
    with engine.connect() as connection:
        # Try a simple query to ensure the connection is fully functional
        connection.execute(text("SELECT 1"))
        print("SUCCESS: Connected to PostgreSQL ('market-db').")
        
except ImportError:
    print("SKIPPED: Could not import database engine (check setup file path).")
except Exception as e:
    print(f"FAILURE: Could not connect to PostgreSQL. Check 'market-db' status/credentials. Error: {e}")

# Note: You'll need 'from sqlalchemy.sql import text' if you run the SELECT 1 line

#==================================================
# Define the stock symbol and the time period
#==================================================
SYMBOL = "MSFT"  # Microsoft Corporation
PERIOD = "5d"    # Last 5 days of data
INTERVAL = "1h"  # Hourly data points

print(f"--- Fetching Data for {SYMBOL} ---")

try:
    # 1. Fetch the data using yfinance.download
    # This returns a pandas DataFrame (df)
    df = yf.download(
        tickers=SYMBOL, 
        period=PERIOD, 
        interval=INTERVAL,
        auto_adjust=True
    )
    
    # 2. Check if the DataFrame is empty
    if df.empty:
        print(f"FAILURE: No data returned for {SYMBOL}. Check the symbol or the time period.")
        sys.exit(1)

    # 3. Print the resulting DataFrame (without using a database)
    print("\nSUCCESS: DataFrame retrieved and printed:")
    print("-----------------------------------------")
    print(df.head())
    print(f"\nDataFrame shape: {df.shape}")

except Exception as e:
    print(f"\nCRITICAL FAILURE: An error occurred during data fetch or print.")
    print(f"Error details: {e}")
    sys.exit(1)