import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv('d:/frontend/backend/.env')

url = os.environ.get("SUPABASE_URL")
# Need service role key to run DDL usually, or we can use raw RPC if configured,
# but we might just try using the REST API if we can, or we can instruct the user.
key = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

try:
    # Attempting to use postgres_changes or rpc to alter table is usually restricted from client.
    # But let's try calling a function if it exists, or suggest manual SQL.
    # As an AI, I can't run raw SQL directly via the JS/Python client safely unless RPC is set up.
    print("Cannot run ALTER TABLE directly via standard Supabase client without a custom RPC function.")
    print("The following SQL needs to be executed in the Supabase SQL Editor:")
    print("ALTER TABLE orders ADD COLUMN store_name VARCHAR(255);")
    print("ALTER TABLE orders ADD COLUMN customer_name VARCHAR(255);")
except Exception as e:
    print(e)
