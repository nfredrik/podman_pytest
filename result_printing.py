
from typing import List, Dict, Any, Tuple

def print_processing_start(strings_count: int) -> None:

    """Print a message indicating the start of string processing.
    Args:
        strings_count: Number of strings to process
    """
    print(f"Starting to process {strings_count} strings...")

def print_results(results: List[Tuple[ str, Dict[str, Any]]]) -> None:
    """Print the detailed results of string processing.
    
    Args:
        results: List of tuples containing (worker_id, input_string, stats)
    """
    print("\n=== Processing Complete ===")
    print(f"Processed {len(results)} strings")
    
    # Print detailed results
    print("\nResults:")
    print("-" * 50)
    for input_string, stats in results:
        print(f"  Content:    '{input_string}'")
        print(f"  Characters: {stats['char_count']}")
        print(f"  Words:      {stats['word_count']}")
        print(f"  Time:       {stats['processing_time']:.2f} seconds")
        print("-" * 50)

def print_summary(results: List[Tuple[ str, Dict[str, Any]]]) -> None:
    """Print the summary statistics of the processing.
    
    Args:
        results: List of tuples containing (worker_id, input_string, stats)
    """
    if not results:
        return
        
    total_chars = sum(stats['char_count'] for  _, stats in results)
    total_words = sum(stats['word_count'] for  _, stats in results)
    total_time = max(stats['processing_time'] for  _, stats in results)
    
    print("\nSummary:")
    print(f"  Total strings processed: {len(results)}")
    print(f"  Total characters: {total_chars}")
    print(f"  Total words: {total_words}")
    print(f"  Total processing time: {total_time:.2f} seconds")
