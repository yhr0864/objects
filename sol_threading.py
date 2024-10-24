import serial
import time
import threading
from collections import deque


class ArduinoCommander:
    def __init__(self, port="COM8", baudrate=9600):
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=0.1)
        self.cmd_queue = deque()

    def append(self, cmd):
        """Add command to queue"""
        self.cmd_queue.append(cmd)

    def run_command_loop(self, timeout=None):
        """
        Run the command-sending loop for specified timeout
        Args:
            timeout: Time in seconds to run the loop, None for infinite
        """
        start_time = time.time()

        while True:
            # Check if timeout exceeded
            if timeout and (time.time() - start_time) > timeout:
                print("timeout")
                break

            # Check for feedback
            if self.arduino.in_waiting:
                data = self.arduino.readline().decode("utf-8").strip()
                if data:
                    print(f"Received: {data}")

            # Check and send commands
            if self.cmd_queue:
                # Wait before sending new command
                time.sleep(1)
                # Get and send command
                cmd = self.cmd_queue.popleft()
                self.arduino.write(bytes(cmd + "\n", "utf-8"))
                print(f"Sent: {cmd}")

            # Small delay to prevent CPU hogging
            time.sleep(0.01)

    def close(self):
        """Close the serial connection"""
        self.arduino.close()


if __name__ == "__main__":
    commander = ArduinoCommander()

    # Start the command loop in a separate thread (run_command_loop will keep running)
    loop_thread = threading.Thread(target=commander.run_command_loop)
    # This ensures the thread will exit when the main program exits
    loop_thread.daemon = True
    loop_thread.start()

    try:
        # Now you can add commands whenever you want
        commander.append("LED1 on")
        time.sleep(2)  # Do other work

        commander.append("motor2 rotate")
        time.sleep(1)  # Do other work

        commander.append("LED1 off")
        time.sleep(0.5)  # Do other work

        commander.append("LED2 on")
        time.sleep(0.5)  # Do other work

        # Keep the main thread running (here just for simulation)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        commander.close()
