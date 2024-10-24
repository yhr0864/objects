import asyncio
import time

# import threading
from functools import wraps


# https://stackoverflow.com/questions/9786102/how-do-i-parallelize-a-simple-python-loop
def async_run_in_executor(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()  # Use the current running event loop
        return await loop.run_in_executor(
            None, f, *args, **kwargs
        )  # Run the blocking function in executor

    return wrapper


@async_run_in_executor
def your_function(timeout):
    start_time = time.time()
    print(f"{timeout} start")
    while True:
        # Check if timeout exceeded
        if timeout and (time.time() - start_time) > timeout:
            print(f"finished {timeout}")
            break


# Main function that keeps gathering tasks from a dynamic list
async def dynamic_gather(task_list):
    while True:
        if task_list:
            # Gather and run all tasks concurrently
            await asyncio.gather(*task_list)
            task_list.clear()  # Clear the list after running tasks
        await asyncio.sleep(0.1)  # Sleep for a while to avoid busy-waiting


# Main function to dynamically add tasks to the list
async def main():
    task_list = []  # Start with an empty list of tasks

    # Start the dynamic gatherer in the background
    asyncio.create_task(dynamic_gather(task_list))

    # Dynamically adding tasks over time
    task_list.append(asyncio.create_task(your_function(10)))
    await asyncio.sleep(2)  # Simulate some delay
    task_list.append(asyncio.create_task(your_function(5)))
    await asyncio.sleep(1)  # Simulate some delay
    task_list.append(asyncio.create_task(your_function(3)))


if __name__ == "__main__":
    asyncio.run(main())
