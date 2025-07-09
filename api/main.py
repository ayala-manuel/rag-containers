# api/main.py
from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Mercados Qdrant API")

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)