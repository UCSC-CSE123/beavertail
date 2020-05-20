import random
import threading


class Register_Tester():
    """Register_Tester is a class that has a set of packets.

      Every `add_time` duration a new Packet is added to the set.
      Every `del_time` duration a Packet is dropped from the set.

      If `add_time` or `remove_time` are negative, then its associated
      action will be ignored (e.g. if add_time == -1 , then no packets are added).

      In addition to adding and removing packets, Register_Tester will update a packet's
      RSSI every `update_time` duration.

      When either a packet is updated or added the callback function prn will be called.
    """

    class Packet():
        def __init__(self, name, strength):
            self.name = hash(name)
            self.strength = float(strength)

    def __init__(self, prn, add_time, del_time, update_time):
        self.devices = set()
        self.thread = None
        self.prn = prn

    def insert_new_packet(self, Packet):
        self.prn(Packet)
        self.devices.add(Packet)

    def insert_new(self, name, strength):
        self.insert_new_packet(self.Packet(name, strength))

    def remove(self):
        if len(self.devices) > 0:
            self.devices.remove(random.sample(self.devices, 1)[0])

    def update(self):
        if len(self.devices) > 0:
            p = random.sample(self.devices, 1)[0]
            self.devices.remove(p)
            p.strength = p.strength + (-0.5 if random.random() < 0.5 else 0.5)
            self.insert_new_packet(p)

    # Calling start_async on the test register starts a new thread
    # That updates this object auto-magically.
    def start_async(self):
        pass
