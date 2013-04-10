from rx import Observable
from rx.testing import TestScheduler, ReactiveTest, is_prime, MockDisposable
from rx.disposables import Disposable, SerialDisposable

on_next = ReactiveTest.on_next
on_completed = ReactiveTest.on_completed
on_error = ReactiveTest.on_error
subscribe = ReactiveTest.subscribe
subscribed = ReactiveTest.subscribed
disposed = ReactiveTest.disposed
created = ReactiveTest.created

def test_observe_on_normal():
    scheduler = TestScheduler()
    xs = scheduler.create_hot_observable(
                        on_next(150, 1),
                        on_next(210, 2),
                        on_completed(250)
                    )

    def create():
        return xs.observe_on(scheduler)
    
    results = scheduler.start(create)
    results.messages.assert_equal(on_next(211, 2), on_completed(251))
    xs.subscriptions.assert_equal(subscribe(200, 251))


# def test_ObserveOn_Error():
#     scheduler = TestScheduler(), ex = 'ex'
#     xs = scheduler.create_hot_observable(
#                         on_next(150, 1),
#                         on_error(210, ex)
#                     )

#     results = scheduler.startWithCreate(function () {
#         return xs.observe_on(scheduler)
#     
#     results.messages.assert_equal(on_error(211, ex))
#     xs.subscriptions.assert_equal(subscribe(200, 211))
# 

# def test_ObserveOn_Empty():
#     scheduler = TestScheduler()
#     xs = scheduler.create_hot_observable(
#                         on_next(150, 1),
#                         on_completed(250)
#                     )

#     results = scheduler.startWithCreate(function () {
#         return xs.observe_on(scheduler)
#     
#     results.messages.assert_equal(on_completed(251))
#     xs.subscriptions.assert_equal(subscribe(200, 251))
# 

# def test_ObserveOn_Never():
#     scheduler = TestScheduler()
#     xs = scheduler.create_hot_observable(
#                         on_next(150, 1)
#                     )

#     results = scheduler.startWithCreate(function () {
#         return xs.observe_on(scheduler)
#     
#     results.messages.assert_equal()
#     xs.subscriptions.assert_equal(subscribe(200, 1000))
# 

# def test_SubscribeOn_Normal():
#     scheduler = TestScheduler()
#     xs = scheduler.create_hot_observable(
#                         on_next(150, 1),
#                         on_next(210, 2),
#                         on_completed(250)
#                     )

#     results = scheduler.startWithCreate(function () {
#         return xs.subscribeOn(scheduler)
#     
#     results.messages.assert_equal(on_next(210, 2), on_completed(250))
#     xs.subscriptions.assert_equal(subscribe(201, 251))
# 

# def test_SubscribeOn_Error():
#     scheduler = TestScheduler(), ex = 'ex'
#     xs = scheduler.create_hot_observable(
#                         on_next(150, 1),
#                         on_error(210, ex)
#                     )

#     results = scheduler.startWithCreate(function () {
#         return xs.subscribeOn(scheduler)
#     
#     results.messages.assert_equal(on_error(210, ex))
#     xs.subscriptions.assert_equal(subscribe(201, 211))
# 

# def test_SubscribeOn_Empty():
#     scheduler = TestScheduler()
#     xs = scheduler.create_hot_observable(
#                         on_next(150, 1),
#                         on_completed(250)
#                     )

#     results = scheduler.startWithCreate(function () {
#         return xs.subscribeOn(scheduler)
#     
#     results.messages.assert_equal(on_completed(250))
#     xs.subscriptions.assert_equal(subscribe(201, 251))
# 

# def test_SubscribeOn_Never():
#     scheduler = TestScheduler()
#     xs = scheduler.create_hot_observable(
#                         on_next(150, 1)
#                     )

#     results = scheduler.startWithCreate(function () {
#         return xs.subscribeOn(scheduler)
#     
#     results.messages.assert_equal()
#     xs.subscriptions.assert_equal(subscribe(201, 1001))
# 

if __name__ == '__main__':
    test_observe_on_normal()