import serial
import time

# Initialize serial connection
arduino = serial.Serial(port="COM8", baudrate=9600, timeout=1)


def send_command(command):
    time.sleep(1)  # Sleep for a second before sending the command
    arduino.write(bytes(command, "utf-8"))


def read_response():

    if arduino.in_waiting > 0:
        data = arduino.readline().decode("utf-8").strip()
        return data
    return None


if __name__ == "__main__":
    cmd1 = "motor1 rotate\r\n"
    cmd2 = "motor2 rotate\r\n"

    send_command(cmd1)
    send_command(cmd2)

    response1 = None
    response2 = None

    while response1 is None or response2 is None:
        response1 = (
            read_response() if response1 is None else print("Received:", response1)
        )
        response2 = (
            read_response() if response2 is None else print("Received:", response2)
        )
        time.sleep(0.1)
