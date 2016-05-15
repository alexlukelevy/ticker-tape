import time


# TODO: add thread locking for __events

class Reporter:
    """
    Receives FeedEvents from FeedHandlers and decides upon
    the order in which to publish FeedEvents.
    """

    def __init__(self, tape):
        self.__events = []
        self.__tape = tape

    def report(self):
        while True:
            self.print_status()
            for e in self.__events:
                self.__tape.display(e.content)

            self.__events = []
            time.sleep(10)

    def receive(self, event):
        print('Reporter receiving event: {}'.format(event))
        self.__events.append(event)

    def print_status(self):
        if self.__events:
            print('{0} new events received'.format(len(self.__events)))
        else:
            print('No new events received')
