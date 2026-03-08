from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import supabase
from routers import users, inventory, orders

app = FastAPI(title="HyperLocal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(inventory.router)
app.include_router(orders.router)

@app.get("/")
async def root():
    return {"message": "Welcome to HyperLocal Backend API"}

@app.get("/health")
async def health_check():
    db_status = "connected" if supabase else "disconnected"
    return {"status": "ok", "database": db_status}

