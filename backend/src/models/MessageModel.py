from .BaseDataModel import BaseDataModel
from .db_schemes import Message
from .enums import DataBaseEnum, MessageRoleEnum
import datetime
from bson.objectid import ObjectId
from .AssetModel import AssetModel


class MessageModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_MESSAGE_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_MESSAGE_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_MESSAGE_NAME.value]
            indexes = Message.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    async def create_message(self, content: str, role: str, conversation_id: str):
        
        if role == "user":
            message_role = MessageRoleEnum.USER.value
        elif role == "assistant":
            message_role = MessageRoleEnum.ASSISTANT.value

        message = Message(
            content=content,
            role=message_role,
            conversation_id=conversation_id
        )

        now = datetime.datetime.utcnow()
        message.createdAt = now
        message.updatedAt = now

        result = await self.collection.insert_one(message.dict(by_alias=True, exclude_unset=True))
        message.id = str(result.inserted_id)

        return message.dict(by_alias=True, exclude_unset=True)

    async def get_messages_by_conversation_id(self, conversation_id: str):

        records = await self.collection.find({"conversation_id": ObjectId(conversation_id)}).to_list(length=None)

        return [
            Message(**record)
            for record in records
        ]
    
    
