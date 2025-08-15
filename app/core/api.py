from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

from database.requests import User

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://butterflyescort1.github.io"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


class CreatingUserItem(BaseModel):
    id: int
    city: str


class DeletingUserItem(BaseModel):
    id: int


@app.get("/user/{id}")
async def get_user_route(id: int) -> Dict[str, Any]:
    user = User(id)
    if not await user.user_exists():
        return {
            "ok": False,
            "message": "User does not exist"
        }
    return {
        "ok": True,
        "data": await user.get_user()
    }


@app.post("/create_user")
async def create_user_route(item: CreatingUserItem) -> Dict[str, Any]:
    user = User(item.id)
    if await user.user_exists():
        return {
            "ok": False,
            "message": "User already exists"
        }
    await user.create_user(item.city)
    return {"ok": True}


@app.delete("/delete_user")
async def delete_user_route(item: DeletingUserItem) -> Dict[str, Any]:
    user = User(item.id)
    if not await user.user_exists():
        return {
            "ok": False,
            "message": "User does not exist"
        }
    await user.delete()
    return {"ok": True}
