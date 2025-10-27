import math
from collections import Counter

def display_time(seconds: float) -> str:
    intervals = [
        ("century", 60 * 60 * 24 * 365 * 100),
        ("year", 60 * 60 * 24 * 365),
        ("month", 60 * 60 * 24 * 31),
        ("day", 60 * 60 * 24),
        ("hour", 60 * 60),
        ("minute", 60),
        ("second", 1),
    ]

    if seconds < 1:
        return "less than a second"

    parts = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            # handle irregular plural
            if name == "century":
                unit = "century" if value == 1 else "centuries"
            else:
                unit = name if value == 1 else name + "s"

            parts.append(f"{value:,.0f} {unit}")

    return " ".join(parts)


def guesses_to_score(guesses: float) -> int:
    DELTA = 5
    if guesses < 1e3 + DELTA:
        return 0
    elif guesses < 1e6 + DELTA:
        return 1
    elif guesses < 1e8 + DELTA:
        return 2
    elif guesses < 1e10 + DELTA:
        return 3
    else:
        return 4

def estimate_attack_times(guesses: float) -> dict:
    crack_times_seconds = {
        "online_throttling_100_per_hour": guesses / (100 / 3600),
    }

    crack_times_display = {
        scenario: display_time(seconds)
        for scenario, seconds in crack_times_seconds.items()
    }

    return {
        "crack_times_seconds": crack_times_seconds,
        "crack_times_display": crack_times_display,
        "score": guesses_to_score(guesses),
    }

def check_password_entropy(pwd: str):
    freq = Counter(pwd)
    total = len(pwd)
    
    entropy_per_char = -sum(
        (count / total) * math.log2(count / total) for count in freq.values()
    ) if total > 0 else 0
    total_entropy = entropy_per_char * total

    total_guesses = 0.5 * (2 ** total_entropy)
    results = estimate_attack_times(total_guesses)

    time_display = results["crack_times_display"]["c"]
    time_seconds = results["crack_times_seconds"]["online_throttling_100_per_hour"]

    print(f"[Shannon] {pwd=}, per_char_entropy={entropy_per_char:.2f}, total_entropy={total_entropy:.2f} bits, time={time_display}")
    return results["score"], time_display, time_seconds

def check_password_min_entropy(pwd: str):
    freq = Counter(pwd)
    total = len(pwd)
    if total == 0:
        return 0, "N/A", 0

    max_prob = max(count / total for count in freq.values())
    entropy_per_char = -math.log2(max_prob)
    total_entropy = entropy_per_char * total

    total_guesses = 0.5 * (2 ** total_entropy)
    results = estimate_attack_times(total_guesses)

    time_display = results["crack_times_display"]["online_throttling_100_per_hour"]
    time_seconds = results["crack_times_seconds"]["online_throttling_100_per_hour"]

    print(f"[Min]     {pwd=}, per_char_entropy={entropy_per_char:.2f}, total_entropy={total_entropy:.2f} bits, time={time_display}")
    return results["score"], time_display, time_seconds

