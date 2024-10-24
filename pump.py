import os

from qmixsdk import qmixbus
from qmixsdk import qmixpump
from qmixsdk import qmixvalve
from qmixsdk.qmixbus import UnitPrefix, TimeUnit


class SyringePump:
    def __init__(self, config_file="Nemesys_M_1"):
        # Get the absolute path to config_file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.deviceconfig = os.path.join(script_dir, config_file)
        print("Opening bus with deviceconfig ", self.deviceconfig)

        # Opening the connection to the devices
        self.bus = qmixbus.Bus()
        self.bus.open(self.deviceconfig, "")

        # Lookup devices
        print("Looking up devices...")
        self.pump = qmixpump.Pump()
        self.pump.lookup_by_name("Nemesys_M_1_Pump")
        self.pumpcount = qmixpump.Pump.get_no_of_pumps()
        print("Number of pumps: ", self.pumpcount)
        for i in range(self.pumpcount):
            self.pump2 = qmixpump.Pump()
            self.pump2.lookup_by_device_index(i)
            print("Name of pump ", i, " is ", self.pump2.get_device_name())

        # Start communication
        print("Starting bus communication...")
        self.bus.start()

        print("Enabling pump drive...")
        if self.pump.is_in_fault_state():
            self.pump.clear_fault()
        print(self.pump.is_in_fault_state())

        if not self.pump.is_enabled():
            self.pump.enable(True)

    def aspirate(self, max_volume, max_flow):
        pass

    def dispense(self, max_volume, max_flow):
        pass
