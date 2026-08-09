from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time

app = FastAPI(title="QLUX Sovereign Megalopolis API", version="5.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PostModel(BaseModel):
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
        "content": "QLUXメガボリューム最終版バックエンド稼働中。Teranode 1000万TPS全開！ #QLUX #Teranode",
        "likes": 1024
    }
]

@app.get("/api/v5/status")
def system_status():
    return {
        "system": "QLUX Sovereign Megalopolis",
        "status": "ONLINE",
        "tps": "10,000,000",
        "active_ai_nodes": 8192,
        "fee_sats": "< 0.000001",
        "timestamp": time.time()
    }

@app.get("/api/v5/posts")
def get_posts():
    return {"posts": db_posts}

@app.post("/api/v5/posts")
def add_post(post: PostModel):
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
