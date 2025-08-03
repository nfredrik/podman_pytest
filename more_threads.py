"""
A simple program that demonstrates concurrent execution using multiple threads.
Each thread processes a string from the input list and puts the result in a queue.

Usage:
    python more_threads.py "string1" "string2" "string3"
"""
import threading
import queue
import time
import random
import argparse
from typing import List, Tuple, Dict, Any

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

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process strings using multiple threads')
    parser.add_argument('strings', metavar='STRING', nargs='+',
                       help='List of strings to process (each in separate thread)')
    parser.add_argument('--max-threads', type=int, default=5,
                       help='Maximum number of concurrent threads (default: 5)')
    
    args = parser.parse_args()
    
    # Use the provided strings
    strings_to_process = args.strings
    max_threads = min(args.max_threads, len(strings_to_process))
    
    print(f"Starting to process {len(strings_to_process)} strings using {max_threads} threads...")
    
    # Create a queue for results
    result_queue = queue.Queue()
    
    # Create and start threads
    threads = []
    for i, input_string in enumerate(strings_to_process):
        # Wait if we've reached max threads
        while len(threads) >= max_threads:
            # Check for finished threads
            for t in threads[:]:
                if not t.is_alive():
                    t.join()
                    threads.remove(t)
            if len(threads) >= max_threads:
                time.sleep(0.1)
        
        t = threading.Thread(
            target=worker,
            args=(i, input_string, result_queue)
        )
        t.daemon = True  # Allow program to exit even if threads are running
        threads.append(t)
        t.start()
    
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
    print("\n=== Processing Complete ===")
    print(f"Processed {len(results)} strings")
    
    # Print detailed results
    print("\nResults:")
    print("-" * 50)
    for worker_id, input_string, stats in results:
        print(f"String {worker_id}:")
        print(f"  Content:    '{input_string}'")
        print(f"  Characters: {stats['char_count']}")
        print(f"  Words:      {stats['word_count']}")
        print(f"  Time:       {stats['processing_time']:.2f} seconds")
        print("-" * 50)
    
    # Print statistics
    if results:
        total_chars = sum(stats['char_count'] for _, _, stats in results)
        total_words = sum(stats['word_count'] for _, _, stats in results)
        total_time = max(stats['processing_time'] for _, _, stats in results)
        
        print("\nSummary:")
        print(f"  Total strings processed: {len(results)}")
        print(f"  Total characters: {total_chars}")
        print(f"  Total words: {total_words}")
        print(f"  Total processing time: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()