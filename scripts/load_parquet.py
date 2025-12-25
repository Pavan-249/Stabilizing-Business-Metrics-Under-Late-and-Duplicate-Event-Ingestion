import duckdb
import os

con = duckdb.connect('ticket_sales.duckdb')

print("Loading Parquet files to DuckDB")

# Create schema if not exists
con.execute("CREATE SCHEMA IF NOT EXISTS raw")

# Check if parquet files exist
parquet_path = 'data/streaming_output/**/*.parquet'
file_count = con.execute(f"""
    SELECT COUNT(*) FROM read_parquet('{parquet_path}')
""").fetchone()[0]

print(f"Found {file_count} records in parquet files")


con.execute(f"""
    CREATE OR REPLACE TABLE raw.ticket_events AS
    SELECT * FROM read_parquet('{parquet_path}')
""")

# Verify
count = con.execute("SELECT COUNT(*) FROM raw.ticket_events").fetchone()[0]
print(f"✓ Loaded {count} records into raw.ticket_events")

# Show sample
print("\nSample data:")
print(con.execute("SELECT * FROM raw.ticket_events LIMIT 3").df())
print('Count of distinct ticket IDs:')
print(con.execute("SELECT COUNT(DISTINCT ticket_id) FROM raw.ticket_events;").fetchone()[0])


con.close()
print("\n✓ Complete!")