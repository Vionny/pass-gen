import os
import json
import random
import unicodedata
import functools

print = functools.partial(print, flush=True)


def read_dict_file(pref):
    path = os.path.join(os.path.dirname(__file__), '..', 'dicts', f'{pref}.json')
    if not os.path.exists(path):
        raise FileNotFoundError(f'Dictionary file not found: {path}')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def clean_keyword(word):
    if not word:
        return ""
    word = str(word)
    return unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('ascii')


def is_ascii(s):
    try:
        s.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False

def apply_leetspeak_global(text, leet_dict, leet_percentage=20, debug=False):
    if isinstance(leet_percentage, list) or isinstance(leet_percentage, tuple):
        leet_percentage = leet_percentage[0]
    leet_percentage = int(leet_percentage)

    chars = list(text)

    leetable_indices = [i for i, c in enumerate(chars) if c.lower() in leet_dict]
    if not leetable_indices:
        return text 

    target = max(1, int(len(leetable_indices) * leet_percentage / 100))
    chosen = random.sample(leetable_indices, min(target, len(leetable_indices)))


    for i in chosen:
        c = chars[i].lower()
        options = [opt for opt in leet_dict[c] if is_ascii(opt)]
        if options:
            chars[i] = random.choice(options)
            if debug:
                print(f"  Sub at {i}: {text[i]} -> {chars[i]}")

    return ''.join(chars)


def prepare_keywords(raw_keywords):
    cleaned = []
    for w in raw_keywords:
        if isinstance(w, dict):
            val = w.get("input", "")
        else:
            val = w
        cleaned.append(clean_keyword(val))
    return cleaned


def fill_password(raw_keywords, priority_indices, desired_length, debug=False):
    leet_dict = read_dict_file("leet")
    fillers = read_dict_file("fillers")
    symbols = ['_', '-', '=', '.', '|', ':', '@', '+']

    cleaned = prepare_keywords(raw_keywords)
    selected = [cleaned[i] for i in priority_indices if i < len(cleaned)]
    others = [w for i, w in enumerate(cleaned) if i not in priority_indices]
    all_keywords = selected + others

    sep = random.choice(symbols)
    combined = sep.join(all_keywords)

    leet_pct = random.randint(10, 30)
    transformed = apply_leetspeak_global(combined, leet_dict, leet_percentage=leet_pct, debug=debug)

    password = transformed[:desired_length]

    rem = desired_length - len(password)
    if rem > 0:
        options = [f for group in fillers.values() for f in group if len(f) <= rem]
        if options:
            filler = random.choice(options)
            if len(filler) < rem:
                filler += ''.join(random.choices('0123456789', k=rem - len(filler)))
        else:
            filler = ''.join(random.choices('0123456789', k=rem))
        password += filler
        if debug:
            print(f"Adding filler '{filler}' to reach desired length")

    elif len(password) > desired_length:
        password = password[:desired_length]
        if debug:
            print(f"Truncating password to desired length: {password}")

    assert len(password) == desired_length, f"Final length {len(password)} != {desired_length}"
    return password

