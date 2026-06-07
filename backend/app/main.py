from fastapi import FastAPI

app = FastAPI(
    title="Infrastructure Defect Segmentation API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to the Infrastructure Defect Segmentation API",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Infrastructure Defect Segmentation API is running."
    }