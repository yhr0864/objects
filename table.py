import serial
import asyncio
import time


################
# 2 solutions:
#     1. instantiate 2 obj and call the function by obj.func()
#     2. only one instance but send different cmd by table.send_cmd("motor1 rotate")
################


class Table:
    def __init__(self, tableID, numBottles, ser):
        self.tableID = tableID
        self.ser = ser
        self.numBottles = numBottles

    def background(f):
        def wrapped(*args, **kwargs):
            return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

        return wrapped

    @background
    def write_read_cmd(self, command, timeout=5):
        # waiting before send
        time.sleep(1)

        self.ser.write(bytes(command + "\n", "utf-8"))

        startTime = time.time()
        # Wait for a response
        # time.time() - startTime < timeout
        while True:
            data = self.ser.readline().decode("utf-8").strip()
            if data:  # Check if data is received
                return data
        return "Timeout Error"

    def rotate(self):
        command = f"motor{self.tableID} rotate"
        feedback = self.write_read_cmd(command)
        print("Received: ", feedback)

    def home(self):
        command = f"motor{self.tableID} home"
        feedback = self.write_read_cmd(command)
        print("Received: ", feedback)


if __name__ == "__main__":
    # Initialize serial connection
    ser = serial.Serial(port="COM8", baudrate=9600, timeout=1)

    # Initialize tables
    table_pump = Table(tableID=1, numBottles=2, ser=ser)
    table_measure = Table(tableID=2, numBottles=6, ser=ser)

    # table_pump.rotate()
    table_measure.rotate()

    while True:
        time.sleep(1)
