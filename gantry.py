import telnetlib
import sys
import time


# 2. read from .config or .JSON
# excl_ip = config.EXCL_IP
# excl_port = config.EXCL_PORT


class Gantry:
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


if __name__ == "__main__":
    gantry = Gantry()
    print(gantry.excl_ip, gantry.excl_port)
