import threading
import time

# Function for each thread
def worker_thread(thread_name, delay):
    for i in range(5):
        time.sleep(delay)  # Simulate a delay
        print(f"{thread_name}: {i}")
    print(f"{thread_name} has finished!")  # Print when thread finishes

# Create threads
thread1 = threading.Thread(target=worker_thread, args=("Thread-1", 1))
thread2 = threading.Thread(target=worker_thread, args=("Thread-2", 2))

# Start threads
thread1.start()
thread2.start()

# Main program continues without waiting for threads to finish
print("Threads have started!")
