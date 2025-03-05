from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import router as auth_router
from app.electricity.routes import router as electricity_router

# Create FastAPI app
app = FastAPI(
    title="IoT One Meter API",
    description="API for authenticating users and retrieving electricity usage data from Firebase Realtime Database",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(electricity_router, prefix="/electricity", tags=["electricity usage"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to IoT One Meter API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)