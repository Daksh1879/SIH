from fastapi import FastAPI

app = FastAPI(title="Legal Metrology Rule Engine")

@app.get("/")
def read_root():
    return {"status": "Rule engine running"}

@app.post("/validate")
def validate(data: dict):
    return {"status": "received", "data": data}
