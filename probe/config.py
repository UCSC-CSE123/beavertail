import probe
"""
This file defines configuration variables for probepi.
"""

"""Send a passenger count to the remote server every {x} seconds"""
BEAVERTAIL_PING_INTERVAL = 15

"""
Consider a device "present" if it has been seen in the last
{BEAVERTAIL_DEV_KEEPALIVE} seconds and if when it was seen the device had a RSSI
greater than {BEAVERTAIL_DEV_KEEPALIVE}. These configuration options are not
used by all adapters.
"""
BEAVERTAIL_DEV_KEEPALIVE = 90
BEAVERTAIL_SIG_THRESHOLD = -60

"""
Hostname and port of the beavertail gRPC service. The port that the service
listens on is configured in ../docker-compose.yml and is port 3000 by default.
"""
BEAVERTAIL_HOSTNAME = 'beavertail.natan.la:3000'

"""
Adapter to use to analyze sniffed probe requests. A number of adapters are
available that utilize different techniques; refer to the documentation.
"""
BEAVERTAIL_ADAPTER = probe.NaiveFrequencyCounter

"""
These options are passed to the adapter specified above. Options available vary
by adapter, refer to the documentation.
"""
BEAVERTAIL_ADAPTER_CONFIG = {}
