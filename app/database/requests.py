from typing import Any, List, Dict, Optional

from .models import FileTable, OrderTable, UserTable


class User:
    def __init__(self, id: int):
        self.id = id
    
    async def user_exists(self) -> bool:
        return await UserTable.filter(id=self.id).exists()
    
    async def create_user(self, city: str) -> None:
        await UserTable.create(
            id=self.id,
            city=city
        )
    
    async def get_user(self) -> Dict[str, Any]:
        return await UserTable.filter(id=self.id).first().values()
    
    async def delete(self) -> None:
        await UserTable.filter(id=self.id).delete()


class Order:
    _PAYMENT_IS_REQUIRED_TEXT = "Ожидается оплата🌀"

    def __init__(self, id: Optional[int] = None):
        self.id = id
    
    async def order_exists(self) -> bool:
        if self.id is not None:
            return await OrderTable.filter(id=self.id).exists()
        return False
    
    async def create_order(
        self,
        user_id: int,
        model_name: str,
        photo_link: str,
        service_name: str,
        addservice_name: str,
        amount: int,
        status: str
    ):
        await OrderTable.create(
            mammoth_id=user_id,
            model_name=model_name,
            photo_link=photo_link,
            service_name=service_name,
            addservice_name=addservice_name,
            amount=amount,
            status=status
        )
    
    async def get_order(self) -> Dict[str, Any]:
        if self.id:
            order = await OrderTable.filter(id=self.id).first().values()
            if order["status"] == "new":
                order["status"] = self._PAYMENT_IS_REQUIRED_TEXT
            return order
        return {}
    
    @classmethod
    async def get_user_orders(self, user_id: int) -> List[Dict[str, Any]]:
        orders = await OrderTable.filter(status="new", mammoth_id=user_id).values()
        new_orders = []
        for order in orders:
            if order["status"] == "new":
                order["status"] = self._PAYMENT_IS_REQUIRED_TEXT
            new_orders.append(order)
        return new_orders
    
    async def delete(self) -> None:
        await OrderTable.filter(id=self.id).update(status="cancelled")


class File:
    def __init__(self, id: str):
        self.id = id
    
    async def file_exists(self) -> bool:
        return await FileTable.filter(id=self.id).exists()
    
    async def create_file(self, file_id: str):
        await FileTable.create(
            id=self.id,
            file_id=file_id
        )
    
    async def get_file_id(self) -> str:
        return (await FileTable.get(id=self.id)).file_id
    
    async def delete_file(self) -> str:
        await FileTable.filter(id=self.id).delete()
