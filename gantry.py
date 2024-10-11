import telnetlib
import sys
import time


# 2. read from .config or .JSON
# excl_ip = config.EXCL_IP
# excl_port = config.EXCL_PORT


class Gantry:
    """
    write something here

    """

    def __init__(self, excl_ip="192.168.0.1", excl_port=23):
        self._excl_ip = excl_ip
        self._excl_port = excl_port

    @property
    def excl_ip(self):
        return self._excl_ip

    @excl_ip.setter
    def excl_ip(self, ip):
        if not isinstance(ip, str):
            raise ValueError("ip must be str!")
        self._excl_ip = ip

    @property
    def excl_port(self):
        return self._excl_port

    @excl_port.setter
    def excl_port(self, port):
        if not isinstance(port, int):
            raise ValueError("port must be int!")
        self._excl_port = port

    def connect(self):
        # EXCL_IP = "192.168.0.1"
        # EXCL_PORT = 23
        # instantiate in ordinary way

        tn_client = telnetlib.Telnet(self._excl_ip, self._excl_port)

        return tn_client

    def home(myClient, axis):
        myClient.write(
            "G28 ".encode("ascii")
            + axis.encode("ascii")
            + "G04 P1".encode("ascii")
            + b"\r\n"
        )
        time.sleep(1)
        msg = myClient.read_until("ok".encode("ascii"), 10)
        print(msg)

    @staticmethod
    def quick_stop(myClient):
        myClient.write("M112".encode("ascii") + b"\n")
        msg = myClient.read_until("ok".encode("ascii"), 5)

    def moveX(myClient, X, speed):
        X = str(X)
        speed = str(speed * 60000)
        myClient.write(
            "G1 X".encode("ascii")
            + X.encode("ascii")
            + " F".encode("ascii")
            + speed.encode("ascii")
            + b"\n"
        )
        msg = myClient.read_until("ok".encode("ascii"), 5)

    def moveY(myClient, Y, speed):
        Y = str(Y)
        speed = str(speed * 60000)
        myClient.write(
            "G1 Y".encode("ascii")
            + Y.encode("ascii")
            + " F".encode("ascii")
            + speed.encode("ascii")
            + b"\n"
        )
        msg = myClient.read_until("ok".encode("ascii"), 5)

    def moveZ(myClient, Z, speed):
        Z = str(Z)
        speed = str(speed * 60000)
        myClient.write(
            "G1 Z".encode("ascii")
            + Z.encode("ascii")
            + " F".encode("ascii")
            + speed.encode("ascii")
            + b"\n"
        )
        msg = myClient.read_until("ok".encode("ascii"), 5)

    def g_command(myClient, moveStr):
        myClient.write(moveStr.encode("ascii") + b"\n")
        msg = myClient.read_until("ok".encode("ascii"), 5)


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


class SyringePump:
    pass


class Spinncoater:
    pass


if __name__ == "__main__":
    gantry = Gantry()
    print(gantry.excl_ip, gantry.excl_port)
