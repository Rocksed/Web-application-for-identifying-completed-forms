import requests

url = "http://localhost:5000/get_form"

# Тестовый запрос с совпадением шаблона
data = {"f_name1": "test@example.com", "f_name2": "+7 123 456 78 90"}
response = requests.post(url, data=data)
print("Response for matching template:", response.json())

# Тестовый запрос без совпадения шаблона
data = {"f_name1": "test@example.com", "f_name2": "not_a_phone_number"}
response = requests.post(url, data=data)
print("Response for non-matching template:", response.json())
