from functools import wraps
from bson import ObjectId
from fastapi import HTTPException, status


def is_authorized(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "credentials" in kwargs and kwargs["credentials"] is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
        return func(*args, **kwargs)
    return wrapper

def handler_nosql_id(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "id" in kwargs:
            if not isinstance(kwargs["id"], str):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid ID",
                )
        return func(*args, **kwargs)
    return wrapper


def handler_id_retrieve(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        obj = func(*args, **kwargs)
        if obj and "_id" in obj:
            obj["id"] = str(obj["_id"])
            del obj["_id"]
            for key, value in obj.items():
                if isinstance(value, ObjectId):
                    obj[key] = str(value)
            obj = args[0].model(**obj)
            return obj
        return None

    return wrapper


def handler_id_retrieve_list(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        objs = func(*args, **kwargs)
        new_objs = []
        for obj in objs:
            if obj and "_id" in obj:
                obj["id"] = str(obj["_id"])
                del obj["_id"]
                for key, value in obj.items():
                    if isinstance(value, ObjectId):
                        obj[key] = str(value)
            obj = args[0].model(**obj)
            new_objs.append(obj)
        return new_objs
    return wrapper
