from fastapi import FastAPI

app = FastAPI(
    title="SafePlate API",
    description="Dietary compatibility platform for restaurant menus.",
    version="0.1.0",
)

@app.get("/")
def root():
    return {"message": "Welcome to SafePlate API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}