from fastapi import fastapi

app = FastAPI(
        title = "Team Todo API",
        version = "0.1.0"
        )

@app.get("/")
def root():
    return {"message": "Team Todo API"}
