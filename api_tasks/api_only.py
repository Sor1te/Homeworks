import os
import random

import requests
import pprint
import pygame

from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт
from PIL import Image

server_address = 'http://geocode-maps.yandex.ru/1.x/?'
api_key = '8013b162-6b42-4997-9691-77b7074026e0'
list_geocode = ['Казань', 'Нижний Новгород', 'Москва', 'Ростов-на-Дону', 'Уфа']
poses = []
photos = []
count = 0
# Готовим запрос.
for geocode in list_geocode:
    response = requests.get(
        "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=geocode&format=json")
    geocoder_request = f'{server_address}apikey={api_key}&geocode={geocode}&format=json'

    # Выполняем запрос.
    response = requests.get(geocoder_request)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
        # Получаем первый топоним из ответа геокодера.
        # Согласно описанию ответа, он находится по следующему пути:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]['GeoObject']
        # Полный адрес топонима:
        # pprint.pprint(toponym['boundedBy']['Envelope']['lowerCorner'])
        # pprint.pprint(toponym['boundedBy']['Envelope']['upperCorner'])
        main_x, main_y = map(float, toponym['Point']['pos'].split(' '))
        x1, y1 = map(float, toponym['boundedBy']['Envelope']['lowerCorner'].split(' '))
        x2, y2 = map(float, toponym['boundedBy']['Envelope']['upperCorner'].split(' '))
        pos_x = str(round(float(main_x) - random.randint(0, 100) * 0.01 * round(abs(x2 - x1) / 2, 6), 6))
        pos_y = str(round(float(main_y) - random.randint(0, 100) * 0.01 * round(abs(y2 - y1) / 2, 6), 6))
        poses.append((pos_x, pos_y))
        # Печатаем извлечённые из ответа поля:
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
    delta = "0.01"
    map_params = {
        "ll": ",".join(poses[count]),
        "spn": ",".join([delta, delta]),
        "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
    }
    map_api_server = "https://static-maps.yandex.ru/v1"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)
    # Создадим картинку и тут же ее покажем встроенным просмотрщиком операционной системы
    map_file = f"map{count}.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    count += 1
    photos.append(map_file)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
# Переключаем экран и ждем закрытия окна.
index_photo = random.randint(0, len(photos) - 1)
new_index = 0
running = True
fps = 60
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                new_index = random.randint(0, len(photos) - 1)
                while new_index == index_photo:
                    new_index = random.randint(0, len(photos) - 1)
                index_photo = new_index
            elif event.key == pygame.K_s:
                new_index = random.randint(0, len(photos) - 1)
                while new_index == index_photo:
                    new_index = random.randint(0, len(photos) - 1)
                index_photo = new_index
    screen.blit(pygame.image.load(photos[index_photo]), (0, 0))
    pygame.display.update()
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)
