from __future__ import print_function
from collections import defaultdict, deque
import threading


class Reporter:
    """
    Receives FeedEvents from FeedHandlers and decides upon
    the order in which to publish FeedEvents.
    """

    def __init__(self, tape, lock=threading.Lock()):
        self._events = defaultdict(lambda: deque(maxlen=5))
        self._tape = tape
        self._lock = lock

    def report(self):
        self._lock.acquire()
        try:
            self.print_status()
            for source, events in self._events.items():
                for e in events:
                    for i in range(0, e.repeat):
                        self._tape.display(e.content)

            self._events = []
        finally:
            self._lock.release()

    def receive(self, event):
        self._lock.acquire()
        try:
            print('Reporter receiving event: {}'.format(event))
            self._events[event.source].append(event)
        finally:
            self._lock.release()

    def print_status(self):
        if self._events:
            print('{0} new events received'.format(len(self._events)))
        else:
            print('No new events received')
