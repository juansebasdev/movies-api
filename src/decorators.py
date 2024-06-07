from functools import wraps
from fastapi import HTTPException, status


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
            obj = args[0].model(**obj)
            new_objs.append(obj)
        return new_objs
    return wrapper
