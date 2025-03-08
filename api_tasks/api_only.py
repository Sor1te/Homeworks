import requests

server_address = 'http://geocode-maps.yandex.ru/1.x/?'
api_key = '8013b162-6b42-4997-9691-77b7074026e0'
geocode = input("Введите адрес: ")
# Готовим запрос.
geocoder_request = f'{server_address}apikey={api_key}&geocode={geocode}&format=json'

# Выполняем запрос.
response = requests.get(geocoder_request)
if response:
    # Преобразуем ответ в json-объект
    json_response = response.json()

    # Получаем первый топоним из ответа геокодера.
    # Согласно описанию ответа, он находится по следующему пути:
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    # Полный адрес топонима:
    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    # Координаты центра топонима:
    c1, c2 = [float(i) for i in toponym["Point"]["pos"].split()]
else:
    print("Ошибка выполнения запроса:")
    print(geocoder_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")

server_address = 'http://geocode-maps.yandex.ru/1.x/?'
api_key = '8013b162-6b42-4997-9691-77b7074026e0'
geocode = 'станция метро Москва'
# Готовим запрос.
geocoder_request = f'{server_address}apikey={api_key}&geocode={geocode}&format=json'

A = []
# Выполняем запрос.
response = requests.get(geocoder_request)
if response:
    # Преобразуем ответ в json-объект
    json_response = response.json()
    for i in json_response["response"]["GeoObjectCollection"]["featureMember"]:
        # Получаем первый топоним из ответа геокодера.
        # Согласно описанию ответа, он находится по следующему пути:
        toponym = i["GeoObject"]
        # Полный адрес топонима:
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        # Координаты центра топонима:
        toponym_coodrinates = [float(i) for i in toponym["Point"]["pos"].split()]
        A.append([toponym_address, ((toponym_coodrinates[0] - c1) ** 2 + (toponym_coodrinates[1] - c2) ** 2) ** 0.5])
else:
    print("Ошибка выполнения запроса:")
    print(geocoder_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
print(f"Ближайшая станция метро: {min(A, key=lambda x: x[1])[0]}")