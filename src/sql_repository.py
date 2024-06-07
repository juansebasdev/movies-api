from src.database import SQLDatabase
from src.utils import IRepository


class SQLRepository(IRepository):

    def __init__(self, db, model):
        self.db: SQLDatabase = db
        self.model = model

    def create(self, data):
        obj = self.model(**data)
        self.db.session.add(obj)
        self.db.session.commit()
        return obj

    def get_all(self, filters=None):
        query = self.db.session.query(self.model)
        if filters:
            query = query.filter_by(**filters)
        return query.all()
    
    def get_all_for_user(self, user_id):
        return self.db.session.query(self.model).filter(self.model.owner_id == user_id).all()

    def get(self, id=None, filters=None):
        query = self.db.session.query(self.model)
        if filters:
            query = query.filter_by(**filters)
            return query.first()
        return self.db.session.query(self.model).filter(self.model.id == id).first()

    def update(self, id, data):
        obj = self.db.session.query(self.model).filter(self.model.id == id).first()
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            self.db.session.commit()
            return obj
        else:
            return None