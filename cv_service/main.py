from fastapi import FastAPI

app = FastAPI(title="CV Service")

@app.get("/")
def read_root():
    return {"status": "CV Service running"}

@app.post("/ocr")
def process_ocr(payload: dict):
    return {"status": "success", "data": payload}
