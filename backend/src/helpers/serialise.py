import datetime
from bson import ObjectId
class Serializer:
    @staticmethod
    def serialise(obj):
        """
        Recursively serialises objects to make them JSON serializable.
        Handles ObjectId, datetime, and nested structures.
        """
        if isinstance(obj, dict):
            return {k: Serializer.serialise(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [Serializer.serialise(item) for item in obj]
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        else:
            return str(obj)