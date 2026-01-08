from fastapi import FastAPI
from app.database.session import engine
from app.api.v1.auth import router as auth_router
from app.api.v1.blogs import router as blog_router



app = FastAPI(
    title="Blog Platform API",
    description="LinkedIn-style blog & social feed platform",
    version="1.0.0"
)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "OK",
        "message": "Backend is running 🚀"
    }




@app.get("/db-check", tags=["Health"])
def db_check():
    try:
        with engine.connect() as connection:
            return {"db": "connected ✅"}
    except Exception as e:
        return {"db": "failed ❌", "error": str(e)}
    


app.include_router(auth_router)
app.include_router(blog_router)
