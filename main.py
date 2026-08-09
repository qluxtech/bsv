from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time

app = FastAPI(title="QLUX Sovereign API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
>

class PostCreate(BaseModel):
    name: str
    id_str: str
    content: str
    avatar: str

posts_db = [
    {
        "id": 1,
        "name": "QLUX Sovereign Node",
        "id_str": "@qlux_master",
        "avatar": "Q",
        "time": "たった今",
        "content": "QLUXウルトラメガボリューム版が完全稼働！Teranodeの1000万TPSで世界を圧倒する。 #QLUX #Teranode #BSV",
        "likes": 512
    }
]

@app.get("/api/status")
def get_system_status():
    return {
        "status": "ONLINE",
        "tps": "10,000,000",
        "active_nodes": 14892,
        "fee_sats": "< 0.000001",
        "timestamp": time.time()
    }

@app.get("/api/posts")
def get_posts():
    return {"posts": posts_db}

@app.post("/api/posts")
def create_post(post: PostCreate):
    new_post = {
        "id": len(posts_db) + 1,
        "name": post.name,
        "id_str": post.id_str,
        "avatar": post.avatar,
        "time": "たった今",
        "content": post.content,
        "likes": 0
    }
    posts_db.insert(0, new_post)
    return {"success": True, "post": new_post}

