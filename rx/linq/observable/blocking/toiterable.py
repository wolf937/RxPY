import threading

from rx.blockingobservable import BlockingObservable
from rx.internal import extensionmethod
from rx.internal.enumerator import Enumerator

@extensionmethod(BlockingObservable)
def to_iterable(self):
    """Returns an iterator that can iterate over items emitted by this
    `BlockingObservable`.

    :returns: An iterator that can iterate over the items emitted by this
        `BlockingObservable`.
    :rtype: collections.Iterable
    """

    condition = threading.Condition()
    notifications = []

    def on_next(value):
        condition.acquire()
        notifications.append(value)
        condition.notify() # signal that a new item is available
        condition.release()

    self.observable.materialize().subscribe(on_next)

    def gen():
        while True:
            condition.acquire()
            while not len(notifications):
                condition.wait()
            notification = notifications.pop(0)

            if notification.kind == "E":
                raise notification.exception

            if notification.kind == "C":
                return # StopIteration

            condition.release()
            yield notification.value

    return Enumerator(gen())

@extensionmethod(BlockingObservable)
def __iter__(self):
    """Returns an iterator that can iterate over items emitted by this
    `BlockingObservable`.

    :returns: An iterator that can iterate over the items emitted by this
        `BlockingObservable`.
    :rtype: collections.Iterable
    """

    return self.to_iterable()
