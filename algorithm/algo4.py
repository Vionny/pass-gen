import json
import os
import random
def read_dict_file():
    """Reads a JSON dictionary file for a given preference name."""
    path = f'./dicts/fillers.json'
    if not os.path.exists(path):
        raise FileNotFoundError(f'Dictionary file not found: {path}')
    
    with open(path, 'r') as file:
        return json.load(file)
      
def fill_password(keywords, priority, desired_length):
    selected_keywords = [keywords[i] for i in priority]
    non_priority_keywords = [word for i, word in enumerate(keywords) if i not in priority]

    symbols = ['_', '-', '=', '.']

    # Filler words that include symbols and make sense
    fillers = read_dict_file()

    joined = ""

    def can_add(word):
        return len(joined) + len(word) <= desired_length

    def get_filler(rem):
        """Choose a filler word that fits into the remaining space"""
        available = [f for length, group in fillers.items() if length == rem for f in group]
        return random.choice(available) if available else random.choice(symbols)

    def add_separator():
        remaining = desired_length - len(joined)
        if remaining >= 3 and random.random() < 0.4:  # 40% chance to insert filler
            return get_filler(remaining)
        return random.choice(symbols)

    # Add priority keywords
    for word in selected_keywords:
        if can_add(word):
            joined += word
        sep = add_separator()
        if can_add(sep):
            joined += sep

    # Add non-priority keywords
    for word in non_priority_keywords:
        if can_add(word):
            joined += word
        sep = add_separator()
        if can_add(sep):
            joined += sep

    # Fill up remaining space
    while len(joined) < desired_length:
        rem = desired_length - len(joined)
        fill = get_filler(rem)
        if can_add(fill):
            joined += fill
        else:
            break

    return joined
