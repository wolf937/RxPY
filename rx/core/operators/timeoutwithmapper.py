from typing import Callable

import rx
from rx.core import Observable, AnonymousObservable
from rx.disposables import CompositeDisposable, SingleAssignmentDisposable, SerialDisposable


def _timeout_with_mapper(first_timeout=None, timeout_duration_mapper=None, other=None) -> Callable[[Observable], Observable]:
    """Returns the source observable sequence, switching to the other
    observable sequence if a timeout is signaled.

        res = timeout_with_mapper(rx.timer(500))
        res = timeout_with_mapper(rx.timer(500), lambda x: rx.timer(200))
        res = timeout_with_mapper(rx.timer(500), lambda x: rx.timer(200)), rx.return_value(42))

    Args:
        first_timeout -- [Optional] Observable sequence that represents the
            timeout for the first element. If not provided, this defaults to
            Observable.never().
        timeout_duration_mapper -- [Optional] Selector to retrieve an
            observable sequence that represents the timeout between the
            current element and the next element.
        other -- [Optional] Sequence to return in case of a timeout. If not
            provided, this is set to Observable.throw().

    Returns:
        The source sequence switching to the other sequence in case
    of a timeout.
    """

    first_timeout = first_timeout or rx.never()
    other = other or rx.throw(Exception('Timeout'))

    def timeout_with_mapper(source: Observable) -> Observable:
        def subscribe(observer, scheduler=None):
            subscription = SerialDisposable()
            timer = SerialDisposable()
            original = SingleAssignmentDisposable()

            subscription.disposable = original

            switched = False
            _id = [0]

            def set_timer(timeout):
                my_id = _id[0]

                def timer_wins():
                    return _id[0] == my_id

                d = SingleAssignmentDisposable()
                timer.disposable = d

                def on_next(x):
                    if timer_wins():
                        subscription.disposable = other.subscribe(observer, scheduler)

                    d.dispose()

                def on_error(e):
                    if timer_wins():
                        observer.on_error(e)

                def on_completed():
                    if timer_wins():
                        subscription.disposable = other.subscribe(observer)

                d.disposable = timeout.subscribe_(on_next, on_error, on_completed, scheduler)

            set_timer(first_timeout)

            def observer_wins():
                res = not switched
                if res:
                    _id[0] += 1

                return res

            def on_next(x):
                if observer_wins():
                    observer.on_next(x)
                    timeout = None
                    try:
                        timeout = timeout_duration_mapper(x)
                    except Exception as e:
                        observer.on_error(e)
                        return

                    set_timer(timeout)

            def on_error(error):
                if observer_wins():
                    observer.on_error(error)

            def on_completed():
                if observer_wins():
                    observer.on_completed()

            original.disposable = source.subscribe_(on_next, on_error, on_completed, scheduler)
            return CompositeDisposable(subscription, timer)
        return AnonymousObservable(subscribe)
    return timeout_with_mapper