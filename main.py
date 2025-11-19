import os
from typing import List, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import create_document, get_documents, db
from schemas import Project as ProjectSchema, Contactmessage as ContactSchema

app = FastAPI(title="CSE Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProjectResponse(BaseModel):
    id: str
    title: str
    description: str
    tags: List[str] = []
    github: str | None = None
    demo: str | None = None
    image: str | None = None


@app.get("/")
def read_root():
    return {"message": "CSE Portfolio Backend Running"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


def _serialize(doc: dict) -> dict:
    """Convert MongoDB ObjectId and datetime fields to serializable values"""
    if not doc:
        return {}
    d = dict(doc)
    if "_id" in d:
        d["id"] = str(d.pop("_id"))
    for k, v in list(d.items()):
        if hasattr(v, "isoformat"):
            d[k] = v.isoformat()
    return d


@app.get("/api/projects", response_model=List[ProjectResponse])
def list_projects(limit: int | None = 12):
    try:
        docs = get_documents("project", {}, limit)
        # If empty, provide a small starter set (non-persistent until next creation)
        if not docs:
            starter = [
                {
                    "title": "Neural Style Transfer",
                    "description": "Applied CNN-based style transfer to images with PyTorch, enabling artistic filters in real time.",
                    "tags": ["Python", "PyTorch", "CNN", "Computer Vision"],
                    "github": "https://github.com/",
                    "demo": None,
                    "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=1600&auto=format&fit=crop"
                },
                {
                    "title": "Realtime Chat App",
                    "description": "Full-stack websockets chat with FastAPI and React, featuring rooms, typing indicators, and JWT auth.",
                    "tags": ["FastAPI", "React", "WebSockets", "JWT"],
                    "github": "https://github.com/",
                    "demo": None,
                    "image": "https://images.unsplash.com/photo-1518773553398-650c184e0bb3?q=80&w=1600&auto=format&fit=crop"
                },
                {
                    "title": "Compiler Mini-Project",
                    "description": "Built a tiny compiler front-end: lexer, parser (LL(1)), and AST generator in C++.",
                    "tags": ["C++", "Compilers", "Parsing"],
                    "github": "https://github.com/",
                    "demo": None,
                    "image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=1600&auto=format&fit=crop"
                }
            ]
            # Do not write by default; only return as preview
            return [ProjectResponse(id=str(i), **p) for i, p in enumerate(starter, start=1)]
        return [ProjectResponse(**_serialize(d)) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/contact")
def create_contact(payload: ContactSchema):
    try:
        _id = create_document("contactmessage", payload)
        return {"status": "ok", "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response: dict[str, Any] = {
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
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
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

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
