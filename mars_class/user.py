from requests import get, post, delete, put

print(get('http://localhost:8080/api/users').json())
print(delete('http://localhost:8080/api/users/3').json())
print(post('http://localhost:8080/api/users',
           json={'surname': 'Кто-то', 'name': 'Кто-то',
                 'age': 28,
                 'position': 'Директор',
                 'speciality': 'Тим-лидер',
                 'address': 'Москва', 'email': 'yes_1234@gmail.com'}).json())
print(get('http://localhost:8080/api/users/3').json())
print(put('http://localhost:8080/api/users/3',
           json={'surname': 'Фамилия', 'name': 'Имя',
                 'age': 28,
                 'position': 'Директор',
                 'speciality': 'Тим-лидер',
                 'address': 'Москва', 'email': 'yes_1234@gmail.com'}).json())
print(get('http://localhost:8080/api/users/3').json())