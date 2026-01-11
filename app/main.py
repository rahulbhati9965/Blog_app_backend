from fastapi import FastAPI
from app.database.session import engine
from app.api.v1.auth import router as auth_router
from app.api.v1.blogs import router as blog_router
from app.api.v1.follow import router as follow_router
from app.api.v1.feed import router as feed_router
from app.api.v1.profile import router as profile_router
from app.api.v1.comments import router as comments_router
from app.api.v1.likes import router as likes_router
from app.api.v1.search import router as search_router
from app.api.v1.admin import router as admin_router
from app.api.v1.notifications import router as notifications_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.users import router as users_router







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
    



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # frontend (Vite)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(blog_router)
app.include_router(follow_router)
app.include_router(feed_router)
app.include_router(profile_router)
app.include_router(comments_router)
app.include_router(likes_router)
app.include_router(search_router)
app.include_router(admin_router)
app.include_router(notifications_router)
app.include_router(users_router)
