# TickerTape
A Python library for RaspberryPi that aggregates news from various sources and publishes them to a rolling LED ticker tape.

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

## Running
To run TickerTape 

```
$ sudo python tickertape.py
```

By default, this will schedule the `FeedHandlers` to refresh every 5 minutes and will leave the `Reporter` running indefinitely.
