from edcon.edrive.com_modbus import ComModbus
from edcon.edrive.motion_handler import MotionHandler
from edcon.utils.logging import Logging


class Gripper:
    """
    https://festo-research.gitlab.io/electric-automation/festo-edcon/examples/modbus.html

    """

    def __init__(self, cmmt_ip):
        self._cmmt_ip = cmmt_ip

    @property
    def cmmt_ip(self):
        return self._cmmt_ip

    @cmmt_ip.setter
    def cmmt_ip(self, ip):
        if not isinstance(ip, str):
            raise ValueError("ip must be str!")
        self._cmmt_ip = ip

    def connect(self):
        com = ComModbus(self._cmmt_ip)
        mot = MotionHandler(com)

        mot.acknowledge_faults()
        mot.enable_powerstage()
        mot.referencing_task()
        return mot

    def quick_stop(mot):
        """
        for emergency case
        """
        mot.stop_motion_task()

    def rotate(mot, position, velocity, isAbsolute):
        mot.position_task(position, velocity, absolute=isAbsolute)

    def grasp():
        pass

    def place():
        pass
