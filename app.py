from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import re

app = Flask(__name__)

# Инициализация базы данных
db = TinyDB('templates.json')

# Загрузка тестовых данных
# Замените это на свою реальную базу данных или настройте ее
templates = [
    {"name": "Template 1", "field_name_1": "email", "field_name_2": "phone"},
    {"name": "Template 2", "field_name_1": "date", "field_name_2": "text"},
]

db.insert_multiple(templates)


def validate_field(value):
    # Проверка типа значения
    if re.match(r'^\d{2}.\d{2}.\d{4}$', value):
        return 'date'
    elif re.match(r'^\+7 \d{3} \d{3} \d{2} \d{2}$', value):
        return 'phone'
    elif re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
        return 'email'
    else:
        return 'text'


def find_matching_template(fields):
    for template in db.all():
        template_fields = set(template.keys()) - {'name'}
        if template_fields.issubset(fields.keys()):
            match = True
            for field_name, value in fields.items():
                if field_name in template_fields and validate_field(value) != template[field_name]:
                    match = False
                    break
            if match:
                return template['name']
    return None


@app.route('/get_form', methods=['POST'])
def get_form():
    data = request.form.to_dict()
    matching_template = find_matching_template(data)

    if matching_template:
        return jsonify({"template_name": matching_template})
    else:
        # Типизация полей на лету
        field_types = {field_name: validate_field(value) for field_name, value in data.items()}
        return jsonify(field_types)


if __name__ == '__main__':
    app.run(debug=True)
