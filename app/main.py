from fastapi import  FastAPI
from app.api.router import api_router
from scalar_fastapi import get_scalar_api_reference

app=FastAPI(
    title="Personal Finance API",
    version="0.1.0"
)

app.include_router(api_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/scalar", include_in_schema=False)
def scalar_docs():
    return get_scalar_api_reference(
        openapi_url="/openapi.json",
        title="Personal Finance API – Scalar",
    )