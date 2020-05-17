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


# TODO: Delete this
class ExampleTimerCounter(AbstractCounter):
    def __init__(self):
        self.devices = {}

    def register(self, signal) -> bool:
        self.devices[signal.mac_address] = time.now()

    def count(self) -> (int, float):
        for device, last in self.devices.items():
            if last < five_seconds_ago:
                del self.devices[device]
        return len(self.devices), 99.0


# TODO: Delete this
class ResetCounter(AbstractCounter):
    def __init__(self):
        self.devices = []

    def register(self, signal) -> bool:
        self.devices.append(signal.mac_address)

    def count(self) -> (int, float):
        passengers = len(self.devices)
        self.devices = []
        return passengers, 99.0


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
