from collections import Counter
from enum import Enum
import datetime


class ExperimentType(Enum):
    """
    Represents the different experiment types.

    Baseline: single greedy CoT prompt
    Self-Consistency: applies Self-Consistency, path is chosen through majority vote
    Shuffle-Choices: shuffles label order, path is chosen through majority vote
    Combines: applies Self-Consistency and Shuffle-Choices, path is chosen through majority vote
    """
    BASELINE = "baseline"
    SELF_CONSISTENCY = "self-consistency"
    CHOICE_SHUFFLING = "choice-shuffling"
    COMBINED = "combined"


def most_common_string(strings: list[str]) -> str:
    """
    Returns the String that occurs most often in a list of strings.

    :param strings: the list of strings
    :return: string occurring the most
    """
    counts = Counter(strings)
    most_common = max(counts, key=counts.get)
    return most_common


def get_current_datetime():
    """
    Creates a formatted string of the current date and time

    :return: current date and time as formatted string
    """
    current_time = datetime.datetime.now()
    return current_time.strftime('%Y-%m-%d-%H-%M-%S')
