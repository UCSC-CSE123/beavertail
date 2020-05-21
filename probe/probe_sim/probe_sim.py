import random
import threading
import schedule
import time


class Register_Tester:

    """
      Register_Tester is a class that has a set of packets.

      Every `add_time` seconds a new Packet is added to the set.
      Every `del_time` seconds a Packet is dropped from the set.

      If `add_time` or `remove_time` are negative, then its associated
      action will be ignored (e.g. if add_time == -1 , then no packets are added).

      In addition to adding and removing packets, Register_Tester will update a packet's
      RSSI every `update_time` seconds.

      When either a packet is updated or added the callback function prn will be called.
    """

    class Packet:

        def __init__(self, addr2, strength):
            self.addr2 = hash(addr2)
            self.strength = float(strength)

    def __init__(
        self,
        prn,
        add_time,
        del_time,
        update_time,
        ):

        self.devices = set()
        self.thread = None
        self.add_time = add_time
        self.del_time = del_time
        self.update_time = update_time
        self.prn = prn

    def insert_new_packet(self, Packet):
        self.prn(Packet)
        self.devices.add(Packet)

    def insert_new(self, addr2, strength):
        self.insert_new_packet(self.Packet(addr2, strength))

    def add(self):
        self.insert_new(random.getrandbits(128), random.randint(-127,
                        128))

    def remove(self):
        if len(self.devices) > 0:
            self.devices.remove(random.sample(self.devices, 1)[0])

    def update(self):
        if len(self.devices) > 0:
            p = random.sample(self.devices, 1)[0]
            self.devices.remove(p)
            p.strength = p.strength + ((-0.5 if random.random()
                    < 0.5 else 0.5))
            self.insert_new_packet(p)

    def start_async_helper(self):
        schedule.every(self.add_time).seconds.do(self.add)
        schedule.every(self.del_time).seconds.do(self.remove)
        schedule.every(self.update_time).seconds.do(self.update)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def start_async(self):
        """
        Calling start_async on the test register starts a new thread that updates this object auto-magically.
        """

        t = threading.Thread(target=self.start_async_helper)
        t.start()
