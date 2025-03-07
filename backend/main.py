from fastapi import FastAPI, HTTPException
from asyncpg.pool import create_pool
from dotenv import load_dotenv
import os
import logging
import asyncpg
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Database Configuration
DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "port": os.getenv("DB_PORT", "5432"),
}

DB_POOL = None 

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize DB connection pool."""
    global DB_POOL
    try:
        # Create the connection pool for the application
        DB_POOL = await create_pool(
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=int(DB_CONFIG["port"]),
            database=DB_CONFIG["database"],
            min_size=1,
            max_size=10,
        )
        logger.info("Database connection pool initialized successfully")
    except Exception as e:
        logger.error(f"Database pool initialization failed: {e}")
    yield
    if DB_POOL:
        await DB_POOL.close()

# Apply the startup/shutdown lifecycle
app.router.lifespan_context = lifespan

@app.on_event("startup")
async def startup():
    """Check if the database is accessible and initialized."""
    global DB_POOL
    if DB_POOL is None:
        raise RuntimeError("Database connection is not established.")

    async with DB_POOL.acquire() as conn:
        result = await conn.fetchval("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'users'")
        if result is None:
            logger.error("Database table 'users' is missing! Check if database is properly initialized.")
        else:
            logger.info("Database is properly initialized and table 'users' exists.")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if DB_POOL is None:
        logger.error("Health check failed: Database pool is not initialized")
        raise HTTPException(status_code=500, detail="Database pool is not initialized")
    return {"status": "ok"}

@app.get("/readiness")
async def readiness_check():
    """Readiness check for Kubernetes."""
    if DB_POOL is None:
        logger.error("Readiness check failed: Database pool is not initialized")
        raise HTTPException(status_code=500, detail="Database pool is not initialized")
    return {"status": "ready"}

@app.post("/populate")
async def populate_db(count: int = 1):
    """Populate the database with random user names."""
    if DB_POOL is None:
        logger.error("Database pool is not initialized")
        raise HTTPException(status_code=500, detail="Database connection error")

    async with DB_POOL.acquire() as conn:
        for _ in range(count):
            await conn.execute("INSERT INTO users (name) VALUES ('test_user')")

    return {"message": f"{count} users inserted"}

@app.delete("/delete")
async def delete_users():
    """Delete all users from the database."""
    if DB_POOL is None:
        logger.error("Database pool is not initialized")
        raise HTTPException(status_code=500, detail="Database connection error")

    async with DB_POOL.acquire() as conn:
        await conn.execute("DELETE FROM users")
    return {"message": "All users deleted"}

@app.get("/users")
async def get_users():
    """Retrieve all users from the database."""
    if DB_POOL is None:
        logger.error("Database pool is not initialized")
        raise HTTPException(status_code=500, detail="Database connection error")

    async with DB_POOL.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM users")
    return {"users": [dict(row) for row in rows]}

# Ensure FastAPI app is properly initialized
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
