import asyncio
import serial


class Table:
    def __init__(self, tableID, numBottles, ser):
        self.tableID = tableID
        self.numBottles = numBottles
        self.ser = ser

    async def write_read(self, command, timeout=5):

        self.ser.write(f"{command}\n".encode("utf-8"))

        # Give some time for the device to respond
        await asyncio.sleep(0.1)

        # Timeout check
        try:
            async with asyncio.timeout(timeout):
                while True:
                    # Read the response
                    response = self.ser.readline().decode("utf-8").strip()
                    if response:
                        return response

                    # Allow the event loop to run other tasks
                    await asyncio.sleep(0.1)

        except TimeoutError:
            return "ERROR: Timeout waiting for response"

    async def rotate(self):
        command = f"motor{self.tableID} rotate"
        feedback = await self.write_read(command)
        print(f"Received: {feedback}")

    async def home(self):
        command = f"motor{self.tableID} home"
        feedback = await self.write_read(command)
        print(f"Received: {feedback}")


# Main function that keeps gathering tasks from a dynamic list
async def dynamic_gather(task_list):
    while True:
        if task_list:
            # Gather and run all tasks concurrently
            await asyncio.gather(*task_list)
            task_list.clear()  # Clear the list after running tasks
        await asyncio.sleep(0.1)  # Sleep for a while to avoid busy-waiting


async def main():

    try:
        ser = serial.Serial("COM8", baudrate=9600, timeout=1)

        table_pump = Table(tableID=1, numBottles=2, ser=ser)
        table_measure = Table(tableID=2, numBottles=6, ser=ser)

        # Start with an empty list of tasks
        task_list = []

        # Start the dynamic gatherer in the background
        asyncio.create_task(dynamic_gather(task_list))

        # Dynamically adding tasks over time
        task_list.append(asyncio.create_task(table_pump.rotate()))
        await asyncio.sleep(0.5)  # Simulate some delay
        task_list.append(asyncio.create_task(table_measure.rotate()))

        # await asyncio.gather(table_pump.rotate(), table_measure.rotate())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if "ser" in locals():
            ser.close()


if __name__ == "__main__":
    asyncio.run(main())
