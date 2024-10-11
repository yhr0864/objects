import serial
import time
from multiprocessing import Process


class Table:
    def __init__(self, tableID, numBottles, ser):
        self.tableID = tableID
        self.ser = ser
        self.numBottles = numBottles

    def write_read(self, command):
        # Wait otherwise fails to write
        time.sleep(1)

        # Send data to Arduino
        self.ser.write(bytes(command, "utf-8"))  # Send with newline

        # Wait for a response with timeout handling
        while True:
            try:
                feedback = self.ser.readline().decode("utf-8").strip()
                if feedback:  # Check if data is received
                    return feedback
            except serial.SerialTimeoutException:
                print("Timeout while waiting for data.")
                return "ERROR: No response"

    def rotate(self):
        # if self.numBottles == 2:
        #     command = "5"
        # elif self.numBottles == 6:
        #     command = "6"
        # else:
        #     print("ERROR")
        command = f"Motor_{self.tableID}_rotate"
        feedback = self.write_read(command)
        print("Received:", feedback)

    def home(self):
        if self.numBottles == 2:
            command = "a"
        elif self.numBottles == 6:
            command = "b"
        else:
            print("ERROR")
        feedback = self.write_read(command)
        print("Received:", feedback)


if __name__ == "__main__":

    ser = serial.Serial(port="COM8", baudrate=9600, timeout=1)

    table_pump = Table(tableID=1, numBottles=2, ser=ser)
    table_measure = Table(tableID=2, numBottles=6, ser=ser)

    # only communication process
    # use queue to save the commands
    table_pump.rotate()

    table_measure.rotate()
