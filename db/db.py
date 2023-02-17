import motor.motor_asyncio
from bson import ObjectId

from config import MongoConfig

_CLIENT = motor.motor_asyncio.AsyncIOMotorClient(
    MongoConfig.CONNECTION_STRING, serverSelectionTimeoutMS=5000
)
_COLLECTION = _CLIENT[MongoConfig.DB_NAME][MongoConfig.COLLECTION_NAME]


async def write_in_base(data: dict) -> ObjectId:
    result = await _COLLECTION.insert_one(data)
    return result.inserted_id
