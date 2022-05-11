import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass

from uuid import uuid4

from grapheditor.core.event_system.event_types import EventType

import logging
logger = logging.getLogger('event_system')


EventCallback = typing.Callable[['Event'], None]


@dataclass
class Event:
    """Event is a DTO.
    It is sent by Observer, setting the observer as source and giving datas through a dictionary

    """
    source: 'Observable'
    payload: dict


T = typing.TypeVar('T', bound=EventType)


class IObservable(ABC, typing.Generic[T]):
    """
    Observer pattern (pub/sub)

    Observable is sending events by topic (EventType)
    Listener can subscribe to a topic using callback

    """

    @abstractmethod
    def add_listener(self, event_type: T, callback: EventCallback) -> str:
        """
        Subscribe a callback to a specific type of event of this object

        :param T event_type: The event type to listen. ('topic')
        :param EventCallback callback: The function to call when the event is emitted

        :return str listener_uid This uid is mandatory to remove the listener
        """
        pass

    @abstractmethod
    def remove_listener(self, event_uuid: str) -> None:
        """
        Safely removes a listener from its observer.
        You should always remove a listener when the observer is disposed to avoid memory leaks

        :param str event_uuid: The uid returned by the add_listener
        """
        pass

    @abstractmethod
    def emit(self, event_type: T = None, event: Event = None) -> None:
        """
        Notify all the listeners of an event type, calling the callback with event as parameter

        :param  T event_type:
        :param Event event:
        """
        pass


class IListener(ABC):
    """
    Interface used to enrich a callback with an uid

    """

    @property
    @abstractmethod
    def callback(self) -> EventCallback:
        """
        :return EventCallback: the function called when emit is fired
        """
        pass

    @property
    @abstractmethod
    def uuid(self) -> str:
        """
        :return str: the unique id of the listener, mainly used to look up the listener at remove time
        """
        pass


class Listener(IListener):
    """
    Default implementation of the listener container
    """

    def __init__(self, callback: EventCallback):
        self._uuid = uuid4()
        self._callback = callback

    @property
    def callback(self) -> EventCallback:
        return self._callback

    @property
    def uuid(self) -> str:
        return self._uuid


class Observable(IObservable[T]):

    def __init__(self):
        self._listeners = {}
        self._listeners_by_uuid = {}

    def add_listener(self, event_type: T, callback: EventCallback) -> str:
        listener = Listener(callback)

        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

        self._listeners_by_uuid[listener.uuid] = listener

        return listener.uuid

    def remove_listener(self, event_uuid: str):
        """
        Safely remove listener from the observable to avoid memory leaks
        :param event_uuid:
        :return:
        """

        listener = self._listeners_by_uuid.pop(event_uuid, None)

        if listener is None:
            logger.warning(f"Could not found event: {event_uuid}")
            return

    def emit(self, event_type: T = None, event: Event = None):

        if event_type not in self._listeners:
            self._listeners[event_type] = []

        for listener in self._listeners[event_type]:
            listener.callback(event)


