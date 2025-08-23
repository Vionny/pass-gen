import random
import math

def random_substitute_per_preference(pwd, preferences, loaded_dicts, desired_length):
    """
    Applies substitutions and case transformations to the password based on preferences and dictionaries.

    Args:
        pwd (str): The original password.
        preferences (list of str): User preferences like 'uppercase', 'lowercase', 'leet', etc.
        loaded_dicts (dict): Mapping of preference name to substitution dictionary.
        desired_length (int): Desired final password length.

    Returns:
        str: Modified password.
    """
    modified_pwd = list(pwd)
    used_prefs = set()

    has_upper = "uppercase" in preferences
    has_lower = "lowercase" in preferences

    # XOR: If only one of upper/lower is set
    if has_upper ^ has_lower:
        if has_upper:
            modified_pwd = list(pwd.upper())
            preferences = [p for p in preferences if p != "uppercase"]
        elif has_lower:
            modified_pwd = list(pwd.lower())
            preferences = [p for p in preferences if p != "lowercase"]

    available_indexes = list(range(len(modified_pwd)))
    min_amt = math.floor(desired_length / 4)
    max_amt = math.ceil(desired_length / 2)
    to_change = random.sample(available_indexes, k=(max_amt-min_amt)) 
    # print(available_indexes,to_change)

    for _ in to_change:
        if not available_indexes:
            break  # no more characters to change

        # Pick a preference
        if len(used_prefs) < len(preferences):
            pref = next(p for p in preferences if p not in used_prefs)
            used_prefs.add(pref)
        else:
            pref = random.choice(preferences)

        index = random.choice(available_indexes)
        available_indexes.remove(index)

        current_char = modified_pwd[index]
        # print(index)
        if pref in preferences:
            subst_dict = next((d[pref] for d in loaded_dicts if pref in d), None)

            if subst_dict:
                if current_char in subst_dict:
                    replacement = random.choice(subst_dict[current_char])
                    # print(current_char,replacement)
                    modified_pwd[index] = replacement
            # print(current_char,subst_dict[current_char])
            # if current_char in subst_dict:
            #     replacement = random.choice(subst_dict[current_char])
            #     modified_pwd[index] = replacement
        else:
            # Swap case if no dict
            if current_char.isupper():
                modified_pwd[index] = current_char.lower()
            elif current_char.islower():
                modified_pwd[index] = current_char.upper()
            continue

    return ''.join(modified_pwd)
