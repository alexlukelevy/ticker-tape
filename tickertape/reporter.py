from __future__ import print_function
import threading


class Reporter:
    """
    Receives FeedEvents from FeedHandlers and decides upon
    the order in which to publish FeedEvents.
    """

    def __init__(self, tape, lock=threading.Lock()):
        self._events = []
        self._tape = tape
        self._lock = lock

    def report(self):
        self._lock.acquire()
        try:
            self.print_status()
            for e in self._events:
                self._tape.display(e.content)

            self._events = []
        finally:
            self._lock.release()

    def receive(self, event):
        self._lock.acquire()
        try:
            print('Reporter receiving event: {}'.format(event))
            self._events.append(event)
        finally:
            self._lock.release()

    def print_status(self):
        if self._events:
            print('{0} new events received'.format(len(self._events)))
        else:
            print('No new events received')
