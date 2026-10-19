
from fastapi import FastAPI

app = FastAPI(title="HTTPS Learning Project")


@app.get("/")
def home():
    return {
        "message": "HTTPS is working!",
        "project": "HTTPS-PROJECT",
        "status": "secure connection"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
