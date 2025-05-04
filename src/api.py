from fastapi import FastAPI, Path, Query, Body, Request
from pydantic import BaseModel
from typing import Optional, List
import os
from anthropic import Anthropic
from dotenv import load_dotenv
import json
load_dotenv()

# Create FastAPI instance
app = FastAPI(
    title="My API",
    description="This is a sample API built with FastAPI",
    version="0.1.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "API Support",
        "url": "http://example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Define a Pydantic model
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []

# Define some endpoints
@app.get("/", tags=["root"])
async def root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to my API"}

@app.post("/llm")
async def llm(request: Request):
    body = await request.json()
    
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    response = client.messages.create(
        max_tokens=256,
        system=(body['system'] if 'system' in body else ""),
        messages=(body['messages'] if 'messages' in body else []),
        model="claude-3-5-haiku-latest"
    )
    
    return "\n".join([(msg.text if msg.type == "text" else "") for msg in response.content])


@app.get("/items/", tags=["items"])
async def read_items(skip: int = 0, limit: int = 10):
    """Get a list of items with pagination."""
    return {"skip": skip, "limit": limit, "message": "This would return items"}

@app.get("/items/{item_id}", tags=["items"])
async def read_item(
    item_id: int = Path(..., title="The ID of the item to get", ge=1),
    q: Optional[str] = Query(None, max_length=50)
):
    """Get a specific item by ID with an optional query parameter."""
    return {"item_id": item_id, "q": q}

@app.post("/items/", tags=["items"], response_model=Item)
async def create_item(item: Item = Body(..., example={
    "name": "Foo",
    "description": "An optional description",
    "price": 35.4,
    "tax": 3.2,
    "tags": ["tag1", "tag2"]
})):
    """Create a new item."""
    return item

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "contract":
        # Generate OpenAPI schema
        openapi_schema = app.openapi()
        with open("base_prompts/openapi.json", "w") as f:
            json.dump(openapi_schema, f, indent=2)
    else:
        # Run the app
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
# import os
# from dotenv import load_dotenv
# from fastapi import FastAPI, Request
# from anthropic import Anthropic

# # Load environment variables
# load_dotenv()

# # Create FastAPI app
# app = FastAPI()

# @app.post("/llm")
# async def llm(request: Request):
#     body = await request.json()
    
#     client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
#     response = client.messages.create(
#         max_tokens=256,
#         system=(body['system'] if 'system' in body else ""),
#         messages=(body['messages'] if 'messages' in body else []),
#         model="claude-3-5-haiku-latest"
#     )
    
#     return "\n".join([(msg.text if msg.type == "text" else "") for msg in response.content])
