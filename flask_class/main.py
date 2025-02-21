from flask import Flask, url_for

app = Flask(__name__)


@app.route('/')
def sometinhg():
    return "Миссия Колонизация Марса"


@app.route('/index')
def index():
    return "И на Марсе будут яблони цвести!"


@app.route('/promotion')
def promotion():
    list_words = ['Человечество вырастает из детства.', 'Человечеству мала одна планета.',
                  'Мы сделаем обитаемыми безжизненные пока планеты.', 'И начнем с Марса!', 'Присоединяйся!']
    return '<h1>' + '</br> <h1>'.join(list_words)


@app.route('/promotion_image')
def promotion_image():
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet" 
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                    crossorigin="anonymous">
                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                    <title>Колонизация</title>
                  </head>
                  <body>
                    <h1> Жди нас, Марс! </h1>
                    <img src="{url_for('static', filename='img/img.png')}"
                    </br> <div class="alert alert-dark" role="alert">
                    Человечество вырастает из детства.
                    </div>
                    <div class="alert alert-info" role="alert">
                    Человечеству мала одно планета.
                    </div>
                    <div class="alert alert-secondary " role="alert">
                    Мы сделаем обитаемыми безжизненные планеты.
                    </div>
                    <div class="alert alert-warning " role="alert">
                    И начнем с Марса!
                    </div>
                    <div class="alert alert-danger " role="alert">
                    Присоединяйся!
                    </div>
                  </body>
                </html>'''


@app.route('/image_mars')
def image_mars():
    return f'''<!doctype html>
                    <html lang="en">
                      <head>
                        <title>Привет, Марс!</title>
                      </head>
                      <body>
                        <h1>Жди нас, Марс!</h1>
                        <img src="{url_for('static', filename='img/img.png')}"
                        </br> <p>Вон она какая, красная планета</p>
                      </body>
                    </html>'''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
