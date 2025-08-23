import math
from collections import Counter

def format_time(seconds: float) -> str:
    """Convert seconds to a human-readable string with rounded values."""
    intervals = (
        ('years', 60 * 60 * 24 * 365),
        ('days', 60 * 60 * 24),
        ('hours', 60 * 60),
        ('minutes', 60),
        ('seconds', 1),
    )
    for name, count in intervals:
        if seconds >= count:
            value = seconds / count
            return f"{round(value)} {name}"
    return "less than 1 second"

def check_password_entropy(pwd: str, guesses_per_second: float = 1e10):
    """
    Calculate Shannon entropy, classify strength (0–4), and estimate offline attack time.
    """
    freq = Counter(pwd)
    total = len(pwd)
    # Shannon entropy per character
    entropy = -sum((count / total) * math.log2(count / total) for count in freq.values()) if total > 0 else 0
    total_entropy = entropy * total

    # Offline attack time estimation
    total_guesses = 2 ** total_entropy/10
    time_seconds = total_guesses / guesses_per_second
    time_str = format_time(time_seconds)

    print(f"{len(pwd)=}, {pwd=}, per_char_entropy={entropy:.2f}, total_entropy={total_entropy:.2f} bits")
    print(f"Estimated offline attack time (~{guesses_per_second:.0e} guesses/sec): {time_str}")

    # Strength classification (unchanged)
    if total_entropy < 28:
        strength = 0  # Very Weak
    elif total_entropy < 36:
        strength = 1  # Weak
    elif total_entropy < 60:
        strength = 2  # Reasonable
    elif total_entropy < 128:
        strength = 3  # Strong
    else:
        strength = 4  # Very Strong

    return strength, time_str

# Example usage
