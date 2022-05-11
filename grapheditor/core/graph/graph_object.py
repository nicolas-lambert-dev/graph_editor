import uuid
from abc import ABC, abstractmethod


class IGraphObject(ABC):
    """
    An object with a unique identifier
    Each graph object should implement this interface

    """

    @property
    @abstractmethod
    def uid(self) -> str: pass

    @uid.setter
    @abstractmethod
    def uid(self, uid: str): pass


class BaseGraphObject(IGraphObject):
    """
    Basic implementation of the model interface using uuid library to ensure identifier is unique

    """
    objects_by_uuid = {}

    def __init__(self, uid: str = None):
        self._uid = uuid.uuid4() if uid is None else uid

    @property
    def uid(self) -> str:
        return self._uid

    @uid.setter
    def uid(self, uid: str):
        self._uid = uid

        # Todo: Use the graph model to handle that or a Singleton?
        self.objects_by_uuid[uid] = self

