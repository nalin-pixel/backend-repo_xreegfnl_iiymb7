import os
from typing import List, Optional, Any, Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Helpers
# -----------------------------

def serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc
    d = dict(doc)
    if "_id" in d:
        d["id"] = str(d.pop("_id"))
    return d


def serialize_list(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [serialize_doc(d) for d in docs]


# -----------------------------
# Basic endpoints
# -----------------------------
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


# -----------------------------
# Portfolio API
# -----------------------------
@app.get("/api/team")
def get_team():
    try:
        docs = get_documents("team", {}, limit=1)
        team = serialize_doc(docs[0]) if docs else {}
        return {"team": team}
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/members")
def get_members():
    try:
        docs = get_documents("member")
        return {"members": serialize_list(docs)}
    except Exception as e:
        return {"error": str(e), "members": []}


@app.get("/api/projects")
def get_projects():
    try:
        docs = get_documents("project")
        return {"projects": serialize_list(docs)}
    except Exception as e:
        return {"error": str(e), "projects": []}


@app.post("/api/seed")
def seed_data():
    """Seed sample team, members, and projects if collections are empty"""
    try:
        # If any document exists, skip seeding
        if db is None:
            raise Exception("Database not configured")
        has_team = db["team"].count_documents({}) > 0
        has_members = db["member"].count_documents({}) > 0
        has_projects = db["project"].count_documents({}) > 0
        if has_team and has_members and has_projects:
            return {"status": "ok", "message": "Data already present"}

        if not has_team:
            create_document(
                "team",
                {
                    "name": "Your Team",
                    "tagline": "We craft delightful products.",
                    "about": "A cross‑functional team building modern, human‑centered software.",
                    "website": None,
                    "github": None,
                    "x": None,
                    "linkedin": None,
                },
            )
        if not has_members:
            sample_members = [
                {
                    "name": "Alex Kim",
                    "role": "Product Designer",
                    "bio": "Designing intuitive interfaces and systems.",
                    "avatar": None,
                    "skills": ["Figma", "UX", "Design Systems"],
                },
                {
                    "name": "Sam Patel",
                    "role": "Full‑stack Engineer",
                    "bio": "TypeScript enjoyer and API whisperer.",
                    "avatar": None,
                    "skills": ["React", "FastAPI", "MongoDB"],
                },
                {
                    "name": "Jamie Lee",
                    "role": "ML Engineer",
                    "bio": "Prototyping with LLMs and data pipelines.",
                    "avatar": None,
                    "skills": ["Python", "LLMs", "MLOps"],
                },
            ]
            for m in sample_members:
                create_document("member", m)
        if not has_projects:
            sample_projects = [
                {
                    "title": "Project Nebula",
                    "summary": "Interactive 3D landing with real‑time data.",
                    "cover": None,
                    "repo": None,
                    "demo": None,
                    "members": ["Alex Kim", "Sam Patel"],
                    "tags": ["React", "Spline", "WebGL"],
                },
                {
                    "title": "Atlas API",
                    "summary": "Fast, typed API for internal services.",
                    "cover": None,
                    "repo": None,
                    "demo": None,
                    "members": ["Sam Patel"],
                    "tags": ["FastAPI", "OpenAPI", "Docker"],
                },
            ]
            for p in sample_projects:
                create_document("project", p)
        return {"status": "ok", "message": "Seeded sample data"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": [],
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, "name") else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:  # pragma: no cover
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
