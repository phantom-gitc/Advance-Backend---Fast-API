from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Fast API Service",
    description="A FastAPI backend service",
    version="1.2.1",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


@app.get("/")
def read_root():
    """Root endpoint - Health check"""

    # FAST api convert direct this into JSON

    return {"message": "Welcome to FastAPI", "status": "Healthy"}


@app.get("/about")
def about():
    """Return API Meta-data"""
    return {"Service": "Order-Service", "region": "South-Asia", "Version": "1.2.3"}


@app.get("/order")
def order():
    """List Recent Order"""
    return [
        {"order": {"id": 1}, "items": "Butter Chicken", "status": "Delivered"},
        {"order": {"id": 2}, "items": "Butter Paneer", "status": "On-Process"},
        {"order": {"id": 3}, "items": "Butter Dosa", "status": "Pending"},
    ]


@app.get("/order/status")
def order_status():
    """List Order Status"""

    return {"total_order_today": 1234, "top_order": "Butter-chicken"}


@app.get(
    "/order/active",
    summary="Get Active Order ",
    description=(
        "Retun All Order that are currenty beign Prepared or out for Delivery .."
    ),
    tags=["Orders"],
    response_description="List of active order object",
    deprecated=False,
)
def get_activeOrder():
    """This Docstring also appers in docs"""
    return {
        "active_order": [{"id": 1, "item": "Masala Dosa", "status": "Out for Delivery"}]
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
