from datetime import datetime

import motor.motor_asyncio
from bson import ObjectId

from config import MongoConfig
from consumer.mapper import ExMapper


class MongoDB:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            MongoConfig.CONNECTION_STRING, serverSelectionTimeoutMS=5000
        )
        self.collection = self.client[MongoConfig.DB_NAME][MongoConfig.COLLECTION_NAME]

    async def write_in_base(self, data: dict) -> ObjectId:
        result = await self.collection.insert_one(data)
        return result.inserted_id

    async def get_last_data(self):
        cursor = self.collection.find()
        async for item in cursor.sort("timestamp", -1).limit(1):
            return item

    async def get_data_by_date(self, date_from: datetime, date_to: datetime):
        date_from = date_from.isoformat()
        date_to = date_to.isoformat()
        mapped_items = []
        async for item in self.collection.find({"value.moment": {"$lte": date_to, "$gte": date_from}}):
            mapped_items.append(ExMapper(
                exhauster_data=item["value"]
            ))
        return mapped_items


mongodb = MongoDB()
