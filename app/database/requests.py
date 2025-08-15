from typing import Any, Dict

from .models import UserTable


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
