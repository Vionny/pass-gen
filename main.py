from algorithm.algo2 import validate_input
from algorithm.algo3 import load_preference_dicts
from algorithm.algo4 import fill_password
from algorithm.algo5 import random_substitute_per_preference
from algorithm.algo6 import check_password_entropy
from nicegui import ui

# All available options
all_options = ['Name', 'Birth Place', 'Hobby', 'Favourite Movie','Favourite Food','Favourite Artist','School']
dropdown_rows = []
lvl_labels = ['Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong']
strength_labels = ['Very Weak', 'Weak', 'Moderate', 'Strong', 'Very Strong']

password_generated = []

# Track other components
amount_input = None
length_slider = None
checkbox1 = checkbox2 = checkbox3 = checkbox4 = None

def get_selected_options():
    return [row['dropdown'].value for row in dropdown_rows if row['dropdown'].value]

def add_dropdown_row():
    with dropdown_container:
        with ui.row().classes('items-center gap-4') as row_elem:
            dropdown = ui.select(all_options).props('label="Category"').classes('w-48')
            input_box = ui.input().props('label="Keyword"').classes('w-48')
            checkbox = ui.checkbox().classes('ml-2')

            # Delete button
            def delete_row():
                dropdown_rows.remove(row)
                row_elem.delete()  # remove from UI

            delete_btn = ui.button('❌', on_click=delete_row).props('flat color=negative')

            row = {
                'dropdown': dropdown,
                'input': input_box,
                'checkbox': checkbox,
                'element': row_elem  # optional: keep reference if needed
            }

            dropdown_rows.append(row)


def update_output():
    password_table.rows = [
        {'password': p['password'], 'strength': strength_labels[p['lvl']], 'time':p['time']}
        for p in password_generated
    ]
        
# --- Submit logic ---
def handle_submit():
    password_generated.clear()
    data = {
        'amount': amount_input.value,
        'length': length_slider.value,
        'pref': {
            'upperLowerCase': checkbox1.value,
            'number': checkbox2.value,
            'symbol': checkbox3.value,
        },
        'dropdown_rows': []
    }

    for row in dropdown_rows:
        data['dropdown_rows'].append({
            'selected': row['dropdown'].value,
            'input': row['input'].value,
            'checked': row['checkbox'].value,
        })

    # ui.notify(f'Data: {data}')
    try:
        amount = int(amount_input.value)
    except (ValueError, TypeError):
        ui.notify('❌ Please enter a valid whole number', color='negative')
        return

    keywords = []
    priority = []

    if amount < 3 :
        ui.notify('❌ Generated amount must be at least 3 passwords', color='negative')
    
    for i, row in enumerate(dropdown_rows):
        keyword = row['input'].value.strip()
        if keyword:
            keywords.append(keyword)
            if row['checkbox'].value:
                priority.append(len(keywords) - 1)  # match current index in `keywords`

    desired_length=data['length']
    for i in range(amount):
        # print(i)
        # Call validation
        errMsg = validate_input(keywords, priority,desired_length)
        if(errMsg): ui.notify(f'❌ {errMsg}', color='negative')
        preferences = [k for k in ['symbol', 'number'] if data['pref'].get(k)]
        # print(preferences)

        dicts = load_preference_dicts(preferences)
        password = fill_password(keywords, priority, desired_length)

        new_pwd = random_substitute_per_preference(password, preferences, dicts, desired_length)
        level, time_str = check_password_entropy(new_pwd)
        print("Strength level:", level)

        # print(data,errMsg,dicts)
        print(password,new_pwd)
        password_generated.append({'password': new_pwd, 'lvl': level, 'time': time_str})
    update_output()

# ui.button('Generate', on_click=handle_submit).classes('mt-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700')

ui.query('body').classes('w-full max-w-full')

ui.label("🔢 Password Generator").classes('text-2xl font-bold mb-4')

with ui.row().classes('w-full max-w-full flex-nowrap items-start gap-4'):

    
    # LEFT PANEL - Input controls
    with ui.column().classes('p-4 rounded'):
        ui.label("Amount of numbers to generate").classes('text-lg font-semibold')
        amount_input = ui.input().props('type=number').classes('mb-4 w-64')

        ui.label("Keywords (Checklist to prioritize)").classes('text-lg font-semibold')
        dropdown_container = ui.column()
        add_dropdown_row()
        ui.button('+ Add another', on_click=add_dropdown_row).classes('my-2')

        ui.label("Desired Length").classes('text-lg font-semibold mt-6')
        length_label = ui.label("Length: 12")
        length_slider = ui.slider(min=8, max=22, value=12, on_change=lambda e: length_label.set_text(f"Length: {e.value}")).classes('w-64')

        ui.label("Options").classes('text-lg font-semibold mt-6')
        with ui.row().classes('gap-10'):
            checkbox1 = ui.checkbox('Include uppercase')
        with ui.row().classes('gap-10'):
            checkbox2 = ui.checkbox('Include numbers')
            checkbox3 = ui.checkbox('Include symbols')

        ui.button('Generate', on_click=handle_submit).classes('mt-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700')

    # RIGHT PANEL - Output
    with ui.column().classes('p-4 rounded'):
        ui.label("Generated Passwords").classes('text-lg font-semibold mt-2')

        password_table = ui.table(
            columns=[
                {'name': 'password', 'label': 'Generated Password', 'field': 'password'},
                {'name': 'strength', 'label': 'Strength', 'field': 'strength'},
            ],
            rows=[],
            row_key='password'
        ).classes('mt-2 text-center')

        def clear_output():
            password_generated.clear()
            update_output()
            ui.notify('✅ Output cleared', color='positive')

        ui.button('Clear Output', on_click=clear_output).classes('mb-2 bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600')


ui.run(port=5000)