from fastapi import FastAPI

app = FastAPI(
    title= 'Predictive Maintenance API'
)

@app.get("/health")
def health_status():
    return {"status : ok"}