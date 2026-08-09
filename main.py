from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time

app = FastAPI(title="QLUX Sovereign Supreme API", version="6.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PostSchema(BaseModel):
    name: str
    id_str: str
    content: str
    avatar: str

db_posts = [
    {
        "id": 1,
        "name": "QLUX Sovereign Master",
        "id_str": "@qlux_master",
        "avatar": "Q",
        "time": "たった今",
        "content": "BSV総合技術を完全網羅した究極のバックエンドが稼働中。Teranode 10M TPS全開！ #BSV #Teranode",
        "likes": 2048
    }
]

@app.get("/api/v6/status")
def system_status():
    return {
        "ecosystem": "QLUX Sovereign Megalopolis",
        "status": "ONLINE",
        "teranode_tps": "10,000,000",
        "active_ai_nodes": 16384,
        "fee_sats": "< 0.000001",
        "timestamp": time.time()
    }

@app.get("/api/v6/posts")
def get_posts():
    return {"posts": db_posts}

@app.post("/api/v6/posts")
def add_post(post: PostSchema):
    new_item = {
        "id": len(db_posts) + 1,
        "name": post.name,
        "id_str": post.id_str,
        "avatar": post.avatar,
        "time": "たった今",
        "content": post.content,
        "likes": 0
    }
    db_posts.insert(0, new_item)
    return {"success": True, "post": new_item}
