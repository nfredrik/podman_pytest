import argparse
import difflib
from pprint import pprint
from typing import List, Tuple, Optional
import pandas as pd

def find_closest_match(reference: str, candidates: List[str], threshold: float = 0.4) -> Tuple[Optional[str], float]:
    matches: List[Tuple[str, float]] = [(candidate, difflib.SequenceMatcher(None, reference, candidate).ratio()) for
                                        candidate in candidates]

    # Find the one with the highest score
    best_match, best_score = max(matches, key=lambda x: x[1], default=("", 0.0))

    # Apply threshold for "no match"
    if best_score <= threshold:
        return None, 0.0

    return best_match, best_score


def method_name(excel_filename:str) -> list:
    testfall = pd.read_excel(excel_filename)
    return testfall["Unnamed: 3"].dropna().to_list()


def main(args):
    candidates = method_name(excel_filename='testfiles.xlsx')

    if not candidates:
        print('no testcases in file!')
        exit(0)

    # Example usage
    testcase_candidates = ["apples", "ape", "maple", "banana"]

    references = ['apple', 'oranges', 'bananas']

    for reference in references:
        match, score = find_closest_match(reference, candidates)

        if match is not None:
            print(f'{reference} {match}, {round(number=score,ndigits=2)}')
            candidates.remove(match)

    print('*' * 80)
    print('These could not be found in the test cases:')
    print(candidates)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demo script")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    main(args)
