#!/usr/bin/env python3.6
import abc
import collections
import datetime
import logging
import os.path
import statistics
import sys
import time
import typing

import grpc
import scapy.all

cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(cwd, '..', 'protocols'))
import datagram_pb2  # noqa: E402
import datagram_pb2_grpc  # noqa: E402

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class AbstractCounter(abc.ABC):
    """
    Defines the interface for implementing a counter.
    """

    def register(self, request: scapy.packet.Packet) -> None:
        log.debug(f"Saw device {request.addr2}")
        # request.show()
        return self._register(request)

    @abc.abstractmethod
    def _register(self, request: scapy.packet.Packet) -> None:
        """
        Called for every probe request seen by :class:`scapy.all.AsyncSniffer`.
        """
        # These fields are probably the most interesting:
        #     rssi = request.dBm_AntSignal
        #     mac_addr = request.addr2
        raise NotImplementedError

    @abc.abstractmethod
    def count(self) -> typing.Tuple[int, float]:
        """
        Returns the amount of passengers determined with a confidence
        assessment.

        The confidence assessment is theoretically optional but is reported
        anyway. If the counting method does not have a reliable confidence
        metric, it should be provided as zero.
        """
        raise NotImplementedError


class TimerCounter(AbstractCounter):
    """
    Considers a device present if it has been seen in the last ``duration``
    seconds.
    """
    def __init__(self, duration: int = 90):
        self.duration = 90
        self.devices = {}

    def _register(self, request: scapy.packet.Packet) -> None:
        """
        Called for every probe request seen by :class:`scapy.all.AsyncSniffer`.
        """
        self.devices[hash(request.addr2)] = datetime.datetime.now()

    def _is_recent_enough(self, timestamp):
        lower_bound = datetime.timedelta(seconds=self.duration)
        xsecondsago = datetime.datetime.now() - lower_bound
        return timestamp > xsecondsago

    def count(self) -> typing.Tuple[int, float]:
        """
        Returns the amount of passengers determined with a confidence
        assessment.

        The confidence assessment is theoretically optional but is reported
        anyway. If the counting method does not have a reliable confidence
        metric, it should be provided as zero.
        """
        self.devices = {dev: ts for dev, ts in self.devices.items() if self._is_recent_enough(ts)}
        return (len(self.devices), 0)


class NaiveFrequencyCounter(AbstractCounter):
    """
    Consider a device present if we receive ``remember_after`` probe requests
    each count period. By default, ``remember_after`` is set to 5 sightings.
    """

    def __init__(self, remember_after: int = 1, confident_after: int = 5):
        """
        :param int remember_after: Minimum amount of "sightings" needed to
            consider a device present
        :param int confident_after: 100% confident a device is present
            after being seen this many times
        """
        self.remember_after = remember_after
        self.confident_after = confident_after
        self.devices = collections.Counter()

    def _register(self, request: scapy.packet.Packet) -> None:
        """
        Called for every probe request seen by :class:`scapy.all.AsyncSniffer`.
        """
        # We store the hash of the MAC address instead of the MAC address
        # itself as a weak measure to minize storing any potentially
        # sensitive data
        self.devices[hash(request.addr2)] += 1

    def count(self) -> typing.Tuple[int, float]:
        """
        Returns the amount of passengers determined with a confidence
        assessment.
        """
        seen = list(filter(lambda x: x >= self.remember_after, self.devices.values()))
        # Calculate confidence based on self.confident_after
        # If we have seen a device at least self.confident_after times, we are
        # "100% confident" that the device was present in the interval.
        # Our confidence decreases geometrically per sighting if we have seen
        # it less than self.confident_after times.
        conf = (2**min(0, -(self.confident_after - v)) for v in seen)
        self.devices.clear()
        # Would prefer fmean need python 3.8
        return (len(seen), statistics.mean(conf))


if __name__ == '__main__':
    # TODO: It would make more sense to pull all of these options from a file.
    # They are unlikely to change.
    if len(sys.argv) != 3:
        print(f"{sys.argv[0]} [busid] [interface]")
        print("\tbusid\tbus ID reported to the server")
        print("\tinterface\tnetwork interface to sniff on")
        sys.exit(0)
    _, bus_id, interface = sys.argv

    # Import config here to prevent a recursive import
    import config

    adapter = config.BEAVERTAIL_ADAPTER(**config.BEAVERTAIL_ADAPTER_CONFIG)
    sniff = scapy.all.AsyncSniffer(prn=lambda p: adapter.register(p),
                                   iface=interface,
                                   store=0,
                                   filter='wlan type mgt subtype probe-req')
    sniff.start()
    while True:
        try:
            time.sleep(config.BEAVERTAIL_PING_INTERVAL)
            passengers, confidence = adapter.count()
            log.info(f"Counted {passengers} devices with confidence {confidence}")
            payload = {
                'busID': bus_id,
                'passengerCount': passengers,
                'passengerCountConfidence': confidence,
                'latitude': 37.554947,
                'longitude': -122.271057,
                'timestamp': int(time.time()),
            }
            # TODO: Make this configurable
            with grpc.insecure_channel(config.BEAVERTAIL_HOSTNAME) as ch:
                stub = datagram_pb2_grpc.PushDatagramStub(ch)
                resp = stub.Push(request=datagram_pb2.DatagramPush(**payload))
                log.debug(f"Push status {resp.acknowledgment}")
        except KeyboardInterrupt:
            # TODO: Refactor as signal handler
            print("Shutting down gracefully...")
            sniff.stop()
            sys.exit(0)
