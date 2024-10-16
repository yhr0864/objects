import asyncio
import serial
import time


class Table:
    def __init__(self, tableID, numBottles, ser):
        self.tableID = tableID
        self.numBottles = numBottles
        self.ser = ser

    async def write_read(self, command, timeout=5):

        self.ser.write(f"{command}\n".encode())

        # Give some time for the device to respond
        await asyncio.sleep(0.1)

        # Read response from the serial port
        start_time = asyncio.get_event_loop().time()
        while True:
            if asyncio.get_event_loop().time() - start_time > timeout:
                return "ERROR: Timeout waiting for response"

            # Read the response
            response = self.ser.readline().decode().strip()
            if response:
                return response

            # Wait before trying again
            await asyncio.sleep(0.1)

    async def rotate(self):
        command = f"motor{self.tableID} rotate"
        feedback = await self.write_read(command)
        print(f"Received: {feedback}")

    async def home(self):
        command = f"motor{self.tableID} home"
        feedback = await self.write_read(command)
        print(f"Received: {feedback}")


async def main():
    try:
        # Create a single shared serial connection
        ser = serial.Serial("COM8", baudrate=9600, timeout=1)

        # Create tables, sharing the same serial connection
        table_pump = Table(tableID=1, numBottles=2, ser=ser)
        table_measure = Table(tableID=2, numBottles=6, ser=ser)

        await asyncio.sleep(1)

        # Run tasks concurrently
        await asyncio.gather(
            table_pump.rotate(),
            table_measure.rotate(),
        )

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up by closing the shared serial connection
        if "ser" in locals():
            ser.close()


if __name__ == "__main__":
    asyncio.run(main())
