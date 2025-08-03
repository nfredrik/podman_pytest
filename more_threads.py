"""
A simple program that demonstrates concurrent execution using multiple threads.
Each thread processes a string from the input list and puts the result in a queue.

Usage:
    python more_threads.py "string1" "string2" "string3"
"""
import argparse
import queue
import threading
import time

# Import the printing functions
from result_printing import print_processing_start, print_results, print_summary


def worker(worker_id: int, input_string: str, result_queue: queue.Queue) -> None:
    """
    Worker function that processes a string and puts the result in the queue.
    
    Args:
        worker_id: Unique identifier for the worker
        input_string: String to be processed by this worker
        result_queue: Queue to put results into
    """
    print(f"Worker {worker_id}: Processing string: '{input_string}'")
    
    # Simulate work based on string length
    duration = 0.5 + (len(input_string) * 0.1)  # Base 0.5s + 0.1s per character
    time.sleep(duration)
    
    # Process the string (example: count characters and words)
    char_count = len(input_string)
    word_count = len(input_string.split())
    
    result = (
        worker_id,
        input_string,
        {
            'char_count': char_count,
            'word_count': word_count,
            'processing_time': duration
        }
    )
    result_queue.put(result)
    print(f"Worker {worker_id}: Completed processing '{input_string}'")

def main(args):
    """Main function that processes strings using multiple threads.
    
    Args:
        args: Parsed command line arguments
    """
    # Use the provided strings
    strings_to_process = args.strings
    print_processing_start(len(strings_to_process))
    
    # Create a queue for results
    result_queue = queue.Queue()
    
    # Create and start threads
    threads = []
    for i, input_string in enumerate(strings_to_process):
        # Create and start a new thread for each string
        t = threading.Thread(
            target=worker,
            args=(i, input_string, result_queue),
            daemon=True  # Allow program to exit even if threads are running
        )
        threads.append(t)
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    # Get all results from the queue
    results =[result_queue.get() for _ in range(result_queue.qsize())]


    # Sort results by worker_id for consistent output
    results.sort(key=lambda x: x[0])
    
    # Print results and summary using the result_printing module
    print_results(results)
    print_summary(results)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process strings using multiple threads')
    #parser.add_argument('strings', metavar='STRING', nargs='+',
    #                    help='List of strings to process (each in separate thread)')
    def split_by_commas(value):
        return [v.strip() for v in value.split(',') if v.strip()]
    
    parser.add_argument('--strings', type=split_by_commas, required=True,
                       help='Specify one or more strings (comma-separated)')
    args = parser.parse_args()
    main(args)