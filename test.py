import serial
import time


# def readlines_from(file):
#     with open(file, "r") as f:
#         for line in f:
#             yield line.strip()


class Table:
    def __init__(self, tableID, numBottles, ser):
        self.tableID = tableID
        self.ser = ser
        self.numBottles = numBottles

    def send_command(self, command):
        time.sleep(1)
        self.ser.write(bytes(command + "\n", "utf-8"))

    def rotate(self, cmd_list: list):
        command = f"motor{self.tableID} rotate"

        cmd_list.append(command)
        self.send_command(cmd_list)

    def home(self):
        command = f"motor{self.tableID} home"
        self.send_command(command)


if __name__ == "__main__":
    # Initialize serial connection
    ser = serial.Serial(port="COM8", baudrate=9600, timeout=1)

    # Initialize tables
    table_pump = Table(tableID=1, numBottles=2, ser=ser)
    table_measure = Table(tableID=2, numBottles=6, ser=ser)

    # Status dictionary to track motor states
    status_dict = {
        "motor1": {"rotation": " ", "home": " "},
        "motor2": {"rotation": " ", "home": " "},
    }

    # Read instructions from file
    # file = "./instruction_list.txt"
    # cmdIt = readlines_from(file)
    # cmd = next(cmdIt)
    cmd_list = []
    cmdIt = iter(cmd_list)
    cmd = next(cmdIt)

    feedback_count = len(cmd_list)
    while True:
        # Check for feedback from Arduino
        if ser.in_waiting:
            feedback = ser.readline().decode("utf-8").strip()
            if feedback:
                feedback_count -= 1
                print(feedback)

                # Parse feedback and update status
                parts = feedback.split(" ")
                if len(parts) >= 2:
                    motor = parts[0].lower()  # Convert to lowercase for comparison
                    action = parts[1].lower()

                    if motor == "motor1":
                        if action == "homing":
                            status_dict["motor1"]["home"] = feedback
                        elif action == "rotation":
                            status_dict["motor1"]["rotation"] = feedback
                    elif motor == "motor2":
                        if action == "homing":
                            status_dict["motor2"]["home"] = feedback
                        elif action == "rotation":
                            status_dict["motor2"]["rotation"] = feedback

                if feedback_count == 0:  # Exit after receiving all feedbacks
                    break

        # Process commands
        if cmd is not None:
            if cmd == "motor1 rotate":
                print("rotate motor1")
                table_pump.rotate()
            elif cmd == "motor2 rotate":
                print("rotate motor2")
                table_measure.rotate()
            elif cmd == "motor1 home":
                print("home motor1")
                table_pump.home()
            elif cmd == "motor2 home":
                print("home motor2")
                table_measure.home()

            try:
                cmd = next(cmdIt)
            except StopIteration:  # End of the iterator
                cmd = None

        # time.sleep(0.01)  # Small delay to prevent CPU overuse

    print(status_dict)
    ser.close()  # Clean up serial connection
