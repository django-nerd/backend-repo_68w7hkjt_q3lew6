import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents

app = FastAPI(title="Athletic E-Commerce API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utility to convert ObjectId to str

def serialize_doc(doc):
    if not doc:
        return doc
    doc = dict(doc)
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc


@app.get("/")
def read_root():
    return {"message": "Athletic E-Commerce Backend Running"}


@app.get("/api/products")
def list_products(featured: Optional[bool] = None, limit: int = 20):
    try:
        query = {}
        if featured is not None:
            query["featured"] = featured
        items = get_documents("product", query, limit)
        return [serialize_doc(i) for i in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class CreateProduct(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    images: List[str] = []
    featured: bool = False
    rating: float = 4.5
    reviews_count: int = 0
    sizes: List[str] = ["6","7","8","9","10","11","12"]
    in_stock: bool = True


@app.post("/api/products")
def create_product(payload: CreateProduct):
    try:
        new_id = create_document("product", payload.model_dump())
        doc = db["product"].find_one({"_id": ObjectId(new_id)})
        return serialize_doc(doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/collections")
def list_collections(limit: int = 10):
    try:
        items = get_documents("collection", {}, limit)
        return [serialize_doc(i) for i in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/athletes")
def list_athletes(limit: int = 10):
    try:
        items = get_documents("athlete", {}, limit)
        return [serialize_doc(i) for i in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class NewsletterPayload(BaseModel):
    email: str


@app.post("/api/newsletter")
def subscribe_newsletter(payload: NewsletterPayload):
    try:
        new_id = create_document("newsletter", payload.model_dump())
        return {"status": "ok", "id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = getattr(db, 'name', "✅ Connected")
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
