'''
Выберите веб-сайт с табличными данными, который вас интересует.
Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
Сохраните извлеченные данные в CSV-файл с помощью модуля csv.

Официальные курсы валют на заданную дату, устанавливаемые ежедневно
'''
from fake_useragent import UserAgent
import requests
from lxml import html
import pandas as pd
import csv

# Определение целевого URL
url = 'https://www.cbr.ru/currency_base/daily/'

# Отправка HTTP GET запроса на целевой URL
ua = UserAgent()
headers = {'User-Agent': ua.chrome}
responce = requests.get(url, headers=headers)

# Парсинг HTML-содержимого ответа с помощью библиотеки lxml
tree = html.fromstring(responce.content)

# Использование выражения XPath для выбора всех строк таблицы в пределах таблицы с классом 'data'
table = tree.xpath("//table[@class='data']//tr")

data = []
for row in table:
    # Использование выражения XPath для выбора одной строки из таблицы и получение текста в виде списка
    cells = row.xpath(".//td/text()")
    if cells:
        currency = {}

        # формат столбца 'код валюты' str->int
        try:
            currency['digital_code'] = int(cells[0])
        except ValueError:
            currency['digital_code'] = None

        currency['letter_code'] = cells[1]

        # формат столбца 'еденицы' str->int
        try:
            currency['units'] = int(cells[2])
        except ValueError:
            currency['units'] = None

        currency['name'] = cells[3]

        # формат столбца 'курс' str->float
        try:
            currency['rate'] = float(cells[4].replace(',', '.'))
        except ValueError:
            currency['rate'] = None

        data.append(currency)


column_names = ['digital_code', 'letter_code', 'units', 'name', 'rate']
df = pd.DataFrame(data, columns=column_names)
print(df)


# Запись файла csv
with open('currency.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=column_names, dialect='excel', delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # Записываем заголовки столбцов
    writer.writeheader()
    # Записываем данные
    writer.writerows(data)