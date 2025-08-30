# logic.py

from algorithm.algo2 import validate_input
from algorithm.algo3 import load_preference_dicts
from algorithm.algo4 import fill_password
from algorithm.algo5 import random_substitute_per_preference
from algorithm.algo6 import check_password_entropy, check_password_min_entropy, display_time

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
    shannon_total_seconds = 0  # ✅ accumulate raw seconds
    min_total_seconds = 0
    for _ in range(amount):
        password = fill_password(keywords, priority, length, dicts)
        shannon_score, shannon_time_str, shannon_time_seconds = check_password_entropy(password)
        min_score, min_time_str, min_time_seconds = check_password_min_entropy(password)

        shannon_total_seconds += shannon_time_seconds  
        min_total_seconds += min_time_seconds 

        result.append({
            "password": password,
            "shannon_strength": shannon_score,
            "shannon_time": shannon_time_str,
            "shannon_time_seconds": shannon_time_seconds,
            "min_strength": min_score,
            "min_time": min_time_str,
            "min_time_seconds": min_time_seconds
        })


    # ✅ compute average after loop
    avg_shannon_seconds = shannon_total_seconds / len(result)
    avg_min_seconds = min_total_seconds / len(result)
    
    avg_shannon_time_str = display_time(avg_shannon_seconds)
    avg_min_time_str = display_time(avg_min_seconds)

    return {
        'passwords': result,
        'average_shannon_time': avg_shannon_time_str,
        'average_shannon_seconds': avg_shannon_seconds,
        'average_min_time': avg_min_time_str,
        'average_min_seconds': avg_min_seconds
    }
