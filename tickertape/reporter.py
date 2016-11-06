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
#            print('Reporting on latest events')
            for source, events in self._events.items():
                print('Reporting for ' + source)
                for e in events:
                    for i in range(0, e.repeat):
                        self._tape.display(e.content)

        finally:
            self._lock.release()

    def receive(self, event):
        self._lock.acquire()
        try:
            print('Reporter receiving event: {}'.format(event))
            self._events[event.source].append(event)
        finally:
            self._lock.release()
