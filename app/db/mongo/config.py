from os import getenv
from typing import List, Type, Optional
from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

client: Optional[AsyncIOMotorClient] = None

def load_models() -> List[Type[Document]]:
    """
    Load and return all document models for Beanie ODM.
    Import models here to avoid circular imports.
    """
    from .documents import Moovie 
    
    return [
        Moovie,
    ]

async def init_mongodb():
    """
    Initialize MongoDB connection and Beanie ODM.
    """
    global client
    
    conn_str = getenv("MONGO_CONN_STR")
    db_name = getenv("MONGO_DB_NAME", "daily_movies")
    
    client = AsyncIOMotorClient(conn_str)
    
    await init_beanie(
        database=client[db_name],
        document_models=load_models()
    )
    
    return client
