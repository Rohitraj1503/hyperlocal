
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv('d:/frontend/backend/.env')

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY") # Use anon key from .env

if not url or not key:
    print("Missing Supabase URL or Key")
    exit(1)

supabase: Client = create_client(url, key)

print("Checking 'orders' table...")
try:
    response = supabase.table("orders").select("*").limit(5).execute()
    print("Sample orders:", response.data)
    if response.data:
        print("Columns in 'orders':", response.data[0].keys())
except Exception as e:
    print("Error checking 'orders':", e)

print("\nChecking 'inventory' table...")
try:
    response = supabase.table("inventory").select("*").limit(1).execute()
    print("Sample inventory:", response.data)
    if response.data:
        print("Columns in 'inventory':", response.data[0].keys())
except Exception as e:
    print("Error checking 'inventory':", e)
