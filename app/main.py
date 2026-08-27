from fastapi import fastapi

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Team Todo API"}
