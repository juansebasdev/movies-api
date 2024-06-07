from abc import ABC, abstractmethod


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class IRepository(ABC):
    @abstractmethod
    def create(self, data):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_all_for_user(self, user_id):
        raise NotImplementedError

    @abstractmethod
    def get(self, id):
        raise NotImplementedError

    @abstractmethod
    def update(self, id, data):
        raise NotImplementedError
