from flask import Flask
from data.users import User
from data.news import News
from data import db_session

db_session.global_init("db/blogs.db")
news = News()
user = User()
user.name = "Пользователь 112434"
user.about = "биография пользователя 1235324"
user.email = "email234@email.ru"
db_sess = db_session.create_session()
db_sess.add(user)
db_sess.commit()

user.name = "Пользователь 2"
user.about = "биография пользователя 34"
user.email = "ema2il@email.ru"
db_sess.add(user)
db_sess.commit()


user = db_sess.query(User).first()
print(user.name)

for user in db_sess.query(User).all():
    print(user)