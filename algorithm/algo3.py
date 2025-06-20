import json
import os

def read_dict_file(pref):
    """Reads a JSON dictionary file for a given preference name."""
    path = f'./dicts/leet_{pref}.json'
    if not os.path.exists(path):
        raise FileNotFoundError(f'Dictionary file not found: {path}')
    
    with open(path, 'r') as file:
        return json.load(file)

def load_preference_dicts(preferences):
    """
    Loads a list of dictionaries based on given preferences.

    Args:
        preferences (list of str): The names of the dict files (without .json).
    
    Returns:
        list of dict: The loaded dictionaries.
    """
    loaded_dicts = []
    
    for pref in preferences:
        try:
            d = read_dict_file(pref)
            loaded_dicts.append({pref: d})
        except Exception as e:
            print(f'⚠️ Failed to load dict for "{pref}": {e}')

    return loaded_dicts
