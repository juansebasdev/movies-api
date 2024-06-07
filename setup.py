import json
import os
from dotenv import load_dotenv

from src.auth.models import User
from src.database import NoSQLDatabase, SQLDatabase
from src.movies.models import Movie

load_dotenv()


def setup():
    DATA_REPOSITORY = os.getenv("DATA_REPOSITORY", None)
    SQL_URL = os.getenv("SQL_URL", None)
    MONGO_URL = os.getenv("MONGO_URL", None)

    if DATA_REPOSITORY == "SQL":
        if SQL_URL is None:
            print("SQL_URL is not set. Please set it to a valid SQL database URL.")
            return
        os.system("alembic upgrade head")
        db = SQLDatabase()
        with open("initial_data.json") as f:
            data = json.load(f)
            users = []
            movies = []
            owner = User(**data["users"].pop(0))
            db.session.add(owner)
            db.session.flush()
            for user in data["users"]:
                users.append(User(**user))
            for movie in data["movies"]:
                movie["owner_id"] = owner.id
                movies.append(Movie(**movie))
            db.session.bulk_save_objects(users)
            db.session.bulk_save_objects(movies)
            db.session.commit()

    elif DATA_REPOSITORY == "NOSQL":
        if MONGO_URL is None:
            print("MONGO_URL is not set. Please set it to a valid MongoDB URL.")
            return
        db = NoSQLDatabase()
        with open("initial_data.json") as f:
            data = json.load(f)
            objs = db.client["movies-api"]["users"].insert_many(data["users"])
            for movie in data["movies"]:
                movie["owner_id"] = objs.inserted_ids[0]
            db.client["movies-api"]["movies"].insert_many(data["movies"])
    else:
        print("DATA_REPOSITORY is not set or has an invalid value. Please set it to either SQL or NOSQL.")


if __name__ == "__main__":
    setup()
