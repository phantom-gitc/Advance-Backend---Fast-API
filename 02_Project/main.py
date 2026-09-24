from fastapi import FastAPI, HTTPException, Query

from data import menu_items
from models import MenuResponse


app = FastAPI(
    title="Chai Point Project",
    description="Read only menu API"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Chai Point API"
    }


@app.get("/menu", response_model=MenuResponse)
def get_menu(
    category: str | None = Query(
        None,
        description="Filter menu items by category"
    )
):
    # If category is provided
    if category:
        filtered = [
            item
            for item in menu_items
            if item["category"].lower() == category.lower()
        ]

        # Category doesn't exist
        if not filtered:
            raise HTTPException(
                status_code=404,
                detail=f"No menu items found for category: {category}"
            )

        return {
            "count": len(filtered),
            "items": filtered
        }

    # Return all menu items
    return {
        "count": len(menu_items),
        "items": menu_items
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
