import serial
import time

arduino = serial.Serial(port="COM8", baudrate=9600, timeout=1)


def write_read(x):
    time.sleep(1)
    # Send data to Arduino
    arduino.write(bytes(x, "utf-8"))  # Send with newline

    # Wait for a response
    while True:
        data = arduino.readline().decode("utf-8").strip()
        if data:  # Check if data is received
            return data


# while True:
# input("Enter a number: ")  # Taking input from user

num2 = "5"

value = write_read(num2)  # Send input and get the response
print("Received:", value)  # Print the response
