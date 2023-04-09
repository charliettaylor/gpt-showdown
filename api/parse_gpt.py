from re import findall
from random import choice

from pydantic import parse

kPATTERN = r"\[[A-Za-z]\]"
kCHOICES = "ABCD"


def parse_gpt(gpt_response: str):
    """
    Parse long-winded GPT responses to single capitalized letters.
    """
    ans = findall(kPATTERN, gpt_response)  # needle, haystack

    if (
        len(ans) < 1 or ans[0][1:-1].upper() not in kCHOICES
    ):  # GPT didn't respond as we expected. Choose a random choice
        return choice(kCHOICES)

    return ans[0][1:-1].upper()


def test():
    responses = {
        "My chosen answer is [A].": "A",
        "Some stuff, some more stuff 123 [5] my answer is [c]": "C",
    }

    total = len(responses.keys())
    correct = 0

    for pre, actual in responses.items():
        parsed = parse_gpt(pre)
        if parsed != actual:
            print(f"Failed test: {pre}. Got {parsed} should be {actual}")
            continue
        correct += 1

    print(f"Passed {correct}/{total}")


if __name__ == "__main__":
    test()
