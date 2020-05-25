# probe

This folder contains Raspberry Pi installation and initialization
instructions. For this project, we are using [Raspbian][raspbian] as our
operating system on [Raspberry Pi Model B+][modelb] boards.

  [Raspbian]: https://projects.raspberrypi.org/en/projects/noobs-install
  [modelb]: https://www.raspberrypi.org/products/raspberry-pi-1-model-b-plus/

## Getting set up

### Software

This project requires at least Python 3.6 to run, and some dependencies.

    $ python3.6 -m venv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt

Note that the script requires root permissions.

    $ sudo $(which python) probe.py my_cool_bus_id my_network_interface_name

Press Ctrl-C to exit the script.

See [config.py](config.py) for settings that you can tweak.

### Hardware

#### External Wifi Adapter

Although the Model B+ includes its own wireless network adapter, it does not
support monitor mode which is necessary in order to intercept wireless packets
for the purpose of people counting. In addition, an adapter in this mode cannot
simultaneously be connected to a network. Thus, a second adapter that supports
monitoring mode is required for our design. Here's a list of supported
[chipsets][chipsets].

  [chipsets]: https://wifivisit.blogspot.com/2019/07/Monitor-Mode-Supported-WiFi-Chipset-Adapter-List.html

#### Enabling Monitor Mode

There are multiple ways to enable monitoring on chipsets, however, many of them
require killing the NetworkManager making it more difficult to maintain a wifi
connection while probing.

##### Simple configuration

To use a given network interface `foo` with `probe.py`, it must be set to
monitor mode first:

    $ sudo ifconfig foo down   # We need to bring it down before setting mode
    $ sudo iwconfig foo mode monitor
    $ sudo ifconfig foo up

These changes may not persist after a reboot.

##### Persisting settings on boot

We can modify some configuration to (1) connect our Raspberry Pi to our
desired wireless network (using `wlan0`, the inbuilt wireless adapter) and to
(2) enable monitoring on `wlan1`, our external interface, at boot time.

The first task requires appending some configuration to
`/etc/wpa_supplicant/wpa_supplicant.conf`. We need the nettwork SSID and
password:

    $ cat >> /etc/wpa_supplicant/wpa_supplicant.conf << EOF
    network={
        ssid="SSID_GOES_HERE"
        psk="PASSWORD_GOES_HERE"
    }
    EOF

For the next task, we append to `/etc/network/interfaces`:

    $ cat >> /etc/network/interfaces << EOF
    allow-hotplug wlan1
     iface wlan1 inet manual
     pre-up iw phy phy1 interface add mon1 type monitor
     pre-up iw dev wlan1 del
     pre-up ifconfig mon1 up
    EOF
