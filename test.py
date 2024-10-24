import time
import _thread


def func(timeout):
    start_time = time.time()
    while True:
        # Check if timeout exceeded
        if timeout and (time.time() - start_time) > timeout:
            print(f"{timeout} finished")
            break


if __name__ == "__main__":
    _thread.start_new_thread(func, (10,))
    _thread.start_new_thread(func, (5,))

    while True:
        time.sleep(1)
