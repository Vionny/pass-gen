# logic.py

from algorithm.algo2 import validate_input
from algorithm.algo3 import load_preference_dicts
from algorithm.algo4 import fill_password
from algorithm.algo5 import random_substitute_per_preference
from algorithm.algo6 import check_password_entropy

def generate_passwords(data):
    try:
        amount = int(data.get('amount', 0))
        length = int(data.get('length', 12))
    except ValueError:
        return {'error': 'Amount and length must be integers'}

    if amount < 3:
        return {'error': 'Generated amount must be at least 3 passwords'}

    dropdown_rows = data.get('dropdown_rows', [])
    keywords = []
    priority = []

    for i, row in enumerate(dropdown_rows):
        keyword = row.get('input', '').strip()
        if keyword:
            keywords.append(keyword)
            if row.get('checked', False):
                priority.append(len(keywords) - 1)

    err_msg = validate_input(keywords, priority, length)
    if err_msg:
        return {'error': err_msg}

    preferences = [k for k in ['symbol', 'number'] if data.get('pref', {}).get(k)]
    dicts = load_preference_dicts(preferences)

    result = []
    for _ in range(amount):
        password = fill_password(keywords, priority, length,dicts)
        # new_pwd = random_substitute_per_preference(password, preferences, dicts, length)
        level,time_str = check_password_entropy(password)
        
        result.append({'password': password, 'strength': level,'time': time_str})

    return {'passwords': result}
