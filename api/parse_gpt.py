from re import findall
from random import choice

from pydantic import parse

kPATTERN = r"\[[A-Za-z]\]"
kCHOICES = "ABCD"


def parse_gpt(gpt_response: str):
    """
    Parse long-winded GPT responses to single capitalized letters.
    """
    if "True" in gpt_response:
        return "A"
    if "False" in gpt_response:
        return "B"

    ans = findall(kPATTERN, gpt_response)  # needle, haystack

    if (
        len(ans) < 1 or ans[0][1:-1].upper() not in kCHOICES
    ):  # GPT didn't respond as we expected. Choose a random choice
        return choice(kCHOICES)

    return ans[0][1:-1].upper()


def test():
    known_responses = {
        "My chosen answer is [A].": "A",
        "Some stuff, some more stuff 123 [5] my answer is [c]": "C",
    }

    correct = 0

    for pre, actual in known_responses.items():
        parsed = parse_gpt(pre)
        if parsed != actual:
            print(f"Failed test: {pre}. Got {parsed} should be {actual}")
            continue
        correct += 1

    random_responses = [
        "This is an example of a GPT response with no regex-able match.",
        "Same with this [1] haha",
    ]

    for response in random_responses:
        parsed = parse_gpt(response)
        if parsed not in kCHOICES:
            print(f"Failed test: {response}. Got {parsed} should be one of {kCHOICES}")
            continue
        correct += 1

    total = len(known_responses.keys()) + len(random_responses)
    print(f"Passed {correct}/{total}")


if __name__ == "__main__":
    test()
