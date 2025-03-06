from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, TypeVar, List, Optional, Any, Type
from beanie import Document

T = TypeVar('T')
"""
Действительно мне нужен репозиторий??
"""
class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def get_by_id(self, id: Any) -> Optional[T]:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[T]:
        pass
    
    @abstractmethod
    async def create(self, entity: T) -> T:
        pass
    
    @abstractmethod
    async def update(self, entity: T) -> T:
        pass
    
    @abstractmethod
    async def delete(self, id: Any) -> None:
        pass

T = TypeVar('T', bound=Document)

class MongoRepository(BaseRepository[T], Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model
    
    async def get_by_id(self, id: Any) -> Optional[T]:
        return await self.model.get(id)
    
    async def get_all(self) -> List[T]:
        return await self.model.find_all().to_list()
    
    async def create(self, entity: T) -> T:
        await entity.insert()
        return entity
    
    async def update(self, entity: T) -> T:
        await entity.save()
        return entity
    
    async def delete(self, id: Any) -> None:
        entity = await self.get_by_id(id)
        if entity:
            await entity.delete()