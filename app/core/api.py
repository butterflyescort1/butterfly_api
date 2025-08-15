from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List

from database.requests import Order, User

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


class CreatingOrderItem(BaseModel):
    mammoth_id: int
    model_name: str
    photo_link: str
    service_name: str
    addservice_name: str
    amount: int
    status: str


class DeletingOrderItem(BaseModel):
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


@app.get("/order/{id}")
async def get_order_route(id: int) -> Dict[str, Any]:
    order = Order(id)
    if not await order.order_exists():
        return {
            "ok": False,
            "message": "Order does not exist"
        }
    return {
        "ok": True,
        "data": await order.get_order()
    }


@app.get("/orders/{user_id}")
async def get_orders_route(user_id: int) -> List[Dict[str, Any]]:
    return await Order.get_user_orders(user_id)


@app.post("/create_order")
async def create_order_route(item: CreatingOrderItem) -> Dict[str, Any]:
    service_names = {
        "hour": "Час🌇",
        "twohours": "Два часа🏙",
        "night": "Ночь🌃",
        "video_call": "Видеозвонок📹"
    }
    await Order().create_order(
        user_id=item.mammoth_id,
        model_name=item.model_name,
        photo_link=item.photo_link,
        service_name=service_names[item.service_name],
        addservice_name=item.addservice_name or "Нет",
        amount=item.amount,
        status="Ожидается оплата🌀"
    )
    return {"ok": True}


@app.delete("/delete_order")
async def delete_order_route(item: DeletingOrderItem) -> Dict[str, Any]:
    order = Order(item.id)
    if await order.order_exists():
        order_data = await order.get_order()
        order_status = order_data.get("status")
        if order_status != "cancelled":
            await order.delete()
            return {"ok": True}
    return {
        "ok": False,
        "message": "Order does not exist or already deleted"
    }
