from fastapi import FastAPI

app = FastAPI(title="AI ops assistant")

@app.get("/")
def health_check():
    return {"status":"running"}
    