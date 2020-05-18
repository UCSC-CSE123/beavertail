#!/usr/bin/env python3.6
import abc
import os.path
import sys
import time
import typing

import scapy.all

cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(cwd, '..', 'protocols'))
import datagram_pb2  # noqa: E402
import datagram_pb2_grpc  # noqa: E402

# Send a passenger count to the remote server every {x} seconds
BEAVERTAIL_PING_INTERVAL = 5

# Consider a device "present" if it has been seen in the last
# {BEAVERTAIL_DEV_KEEPALIVE} seconds and if when it was seen the device had a
# RSSI greater than {BEAVERTAIL_DEV_KEEPALIVE}
BEAVERTAIL_DEV_KEEPALIVE = 90
BEAVERTAIL_SIG_THRESHOLD = -60


class AbstractCounter(abc.ABC):
    """
    Defines the interface for implementing a counter.
    """

    @abstractmethod
    def register(self, request: scapy.packet.Packet) -> None:
        """
        Called for every probe request seen by :class:`scapy.all.AsyncSniffer`.
        """
        # These fields are probably the most interesting:
        #     rssi = request.dBm_AntSignal
        #     mac_addr = request.addr2
        raise NotImplementedError

    @abstractmethod
    def count(self) -> typing.Tuple(int, float):
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

    def register(self, request: scapy.packet.Packet) -> None:
        """
        Called for every probe request seen by :class:`scapy.all.AsyncSniffer`.
        """
        self.devices[hash(request.addr2)] = datetime.datetime.now()

    def _is_recent_enough(self, timestamp):
        lower_bound = datetime.timedelta(seconds=self.duration)
        diff = datetime.datetime.now() - lower_bound
        return diff > datetime.timedelta(0)

    def count(self) -> typing.Tuple(int, float):
        """
        Returns the amount of passengers determined with a confidence
        assessment.

        The confidence assessment is theoretically optional but is reported
        anyway. If the counting method does not have a reliable confidence
        metric, it should be provided as zero.
        """
        self.devices = {dev: ts for dev, ts in self.devices.items() if _is_recent_enough(ts))}
        return (len(self.devices), 0)


class NaiveFrequencyCounter(AbstractCounter):
    """
    Consider a device present if we receive ``remember_after`` probe requests
    each count period. By default, ``remember_after`` is set to 5 sightings.
    """

    def __init__(self, remember_after: int = 5):
        """
        :param int remember_after: Minimum amount of "sightings" needed to
            consider a device present
        """
        self.remember_after = remember_after
        self.devices = collections.Counter()

    def register(self, request: scapy.packet.Packet) -> None:
        """
        Called for every probe request seen by :class:`scapy.all.AsyncSniffer`.
        """
        # We store the hash of the MAC address instead of the MAC address
        # itself as a weak measure to minize storing any potentially
        # sensitive data
        self.devices[hash(request.addr2)] += 1

    def count(self) -> typing.Tuple(int, float):
        """
        Returns the amount of passengers determined with a confidence
        assessment.

        The confidence assessment is theoretically optional but is reported
        anyway. If the counting method does not have a reliable confidence
        metric, it should be provided as zero.
        """
        count = len(lambda x: x > self.remember_after, self.devices.values())
        self.devices.clear()
        return (count, 0)


if __name__ == '__main__':
    # TODO: It would make more sense to pull all of these options from a file.
    # They are unlikely to change.
    if len(sys.argv) != 4:
        print(f"{sys.argv[0]} [busid] [interface] [channel]")
        sys.exit(0)
    _, bus_id, interface, channel = sys.argv

    # TODO: We probably need to use `iw` to set channel on interface.
    # Probemon does this. We don't, yet. We should research if this is even
    # necessary.
    adapter = ResetCounter()
    sniff = scapy.all.AsyncSniffer(prn=lambda p: adapter.register(p),
                                   count=0,
                                   filter='wlan type mgt subtype probe-req')
    sniff.start()
    while True:
        try:
            time.sleep(BEAVERTAIL_PING_INTERVAL)
            passengers, confidence = adapter.count()
            payload = {
                'busID': bus_id,
                'passengerCount': passengers,
                'passengerCountConfidence': confidence,
                'latitude': 37.554947,
                'longitude': -122.271057,
                'timestamp': int(time.time()),
            }
            # TODO: Make this configurable
            with grpc.insecure_channel('beavertail.natan.la:3000') as ch:
                stub = datagram_pb2_grpc.PushDatagramStub(ch)
                resp = stub.Push(request=datagram_pb2.DatagramPush(**payload))
                print(resp.acknowledgement)
        except KeyboardInterrupt:
            # TODO: Refactor as signal handler
            print("Shutting down gracefully...")
            sniff.stop()
            sys.exit(0)
