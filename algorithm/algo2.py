def validate_input(keywords, priority, desired_length):

    # 1. Check if keywords list is empty
    if not keywords:
        return "No valid keywords provided"

    # 2. Check desired length range
    if desired_length < 8 or desired_length > 22:
        return "Length must be between 3 and 25"

    total_priority_length = 0
    try:
        for i in priority:
            total_priority_length += len(keywords[i])
    except IndexError:
        return "Priority index out of range"

    if total_priority_length > desired_length:
        return "Total length of priority keywords must be less than Length"

    # 4. Check if all keywords are alphabetic
    for keyword in keywords:
        if not keyword.isalpha():
            return "Keywords must contain only alphabetic characters"

    # All checks passed
    return None