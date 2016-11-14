# Ticker Tape
A Python library for Raspberry Pi that aggregates news from various sources and publishes them to a rolling LED ticker tape.

## Setup
To get started you will need to first ensure you have a Python 2.7 and then install the following python libraries:
* [feedparser](https://pypi.python.org/pypi/feedparser)
* [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/python)

Once those are installed and you have a working Python 2.7 installation you are good to go. 

## Running
To run Ticker Tape, execute the following from **within the `tickertape` directory**

```
$ sudo python tickertape.py
```

By default, this will schedule the `FeedHandlers` to refresh every 5 minutes and will leave the `Reporter` running indefinitely.

## Design
The library consists on four key components; FeedHandlers, the Reporter, the Tape and the Director.

#### FeedHandlers
A `FeedHandler` consumes news events from a given source (e.g. BBC) and publishes `FeedEvents` to the `Reporter`.

#### Reporter
The `Reporter` is responsible for keeping track of all the latest `FeedEvents` from various sources and reporting the events to the `Tape` when requested.

#### Tape
The `Tape` represents the LED matrix and contains the logic to convert a string to an LED output.

### Director
The `Director` oversees the whole operation and coordinates the threads of the `FeedHandlers` and the `Reporter`.

## Setup
This library makes use of the Raspberry Pi LED matrix [project](https://github.com/hzeller/rpi-rgb-led-matrix) from hzeller.

Please follow the wiring instructions found on that project to configure the LED matrix appropriately.
