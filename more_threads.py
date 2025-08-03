"""
A simple program that demonstrates concurrent execution using multiple threads.
Each thread puts results in a queue that the main thread reads from.
"""
import threading
import queue
import time
import random
from typing import List, Tuple

def worker(worker_id: int, duration: float, result_queue: queue.Queue) -> None:
    """
    Worker function that simulates work and puts the result in the queue.
    
    Args:
        worker_id: Unique identifier for the worker
        duration: How long the task should take (in seconds)
        result_queue: Queue to put results into
    """
    print(f"Worker {worker_id}: Starting task (will take {duration:.1f} seconds)")
    time.sleep(duration)  # Simulate work
    result = (worker_id, f"Task {worker_id} completed after {duration:.1f} seconds")
    result_queue.put(result)
    print(f"Worker {worker_id}: {result[1]}")

def main():
    # Configuration
    num_threads = 5
    max_duration = 3.0  # Maximum duration for each task in seconds
    
    # Create a queue for results
    result_queue = queue.Queue()
    
    # Create and start threads
    threads = []
    for i in range(num_threads):
        duration = random.uniform(0.5, max_duration)
        t = threading.Thread(
            target=worker,
            args=(i, duration, result_queue)
        )
        threads.append(t)
        t.start()
    
    print(f"Started {num_threads} workers...")
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    # Get all results from the queue
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    
    # Sort results by worker_id for consistent output
    results.sort(key=lambda x: x[0])
    
    # Print all results
    print("\nAll tasks completed!")
    for worker_id, result in results:
        print(f"  {result}")

if __name__ == "__main__":
    main()