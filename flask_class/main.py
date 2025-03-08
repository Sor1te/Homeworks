from flask import Flask, url_for, request

app = Flask(__name__)


@app.route('/carousel')
def form_sample():
    return f'''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
          integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
          crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}<!DOCTYPE html>
<html lang="en">
<head>
    <title>Пейзажи Марса</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
</head>
<body>
<center>
    <div class="container">
        <h2>Пейзажи Марса</h2>
        <div id="myCarousel" class="carousel slide" data-ride="carousel">
            <!-- Indicators -->
            <ol class="carousel-indicators">
                <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
                <li data-target="#myCarousel" data-slide-to="1"></li>
                <li data-target="#myCarousel" data-slide-to="2"></li>
            </ol>

            <!-- Wrapper for slides -->
            <div class="carousel-inner">

                <div class="item active">
                    <img src="/static/img/mars1.png" style="width:600%;">
                </div>

                <div class="item">
                    <img src="/static/img/mars2.png" style="width:600%;">
                </div>

                <div class="item">
                    <img src="/static/img/mars3.png" style="width:600%;">
                </div>

            </div>

            <!-- Left and right controls -->
            <a class="left carousel-control" href="#myCarousel" data-slide="prev">
                <span class="glyphicon glyphicon-chevron-left"></span>
                <span class="sr-only">Previous</span>
            </a>
            <a class="right carousel-control" href="#myCarousel" data-slide="next">
                <span class="glyphicon glyphicon-chevron-right"></span>
                <span class="sr-only">Next</span>
            </a>
        </div>
    </div>
</center>

</body>
</html>
'''


from PIL import Image


@app.route('/load_photo', methods=['POST', 'GET'])
def sample_file_upload():
    if request.method == 'GET':
        return f'''<!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link rel="stylesheet"
                  href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                  integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                  crossorigin="anonymous">
            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}"/>
            <title>Пример загрузки файла</title>
        </head>
        <body>
        <center>
            <h1>Загрузим файл</h1>
            <h4>для участия в миссии</h4>
            <div class="main_form">
                <form method="post" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="photo">Выберите файл</label>
                        <input type="file" class="form-control-file" id="photo" name="file">
                    </div>
                    <img src="/static/img/load_photo.png">
                    <button type="submit" class="btn btn-primary">Отправить</button>
                </form>
            </div>
        </center>
        </body>
        </html>'''

    elif request.method == 'POST':
        f = request.files['file']
        new_file = f.read()
        if new_file:
            with open('static/img/new_load_photo.png', 'wb') as file:
                file.write(new_file)
            image = Image.open('static/img/new_load_photo.png')
            new_image = image.resize((320, 320))
            new_image.save('static/img/new_load_photo.png')
            return f'''<html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                <link rel="stylesheet"
                      href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                      integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                      crossorigin="anonymous">
                <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}"/>
                <title>Пример загрузки файла</title>
            </head>
            <body>
            <center>
                <h1>Загрузим файл</h1>
                <h4>для участия в миссии</h4>
                <div class="main_form">
                    <form method="post" enctype="multipart/form-data">
                        <div class="form-group">
                            <label for="photo">Выберите файл</label>
                            <input type="file" class="form-control-file" id="photo" name="file">
                        </div>
                        <img src="/static/img/new_load_photo.png">
                        <button type="submit" class="btn btn-primary">Отправить</button>
                    </form>
                </div>
            </center>
            </body>
            </html>'''
        else:
            return 'Неправильный запрос'


if __name__ == '__main__':
    app.run(port=8008, host='127.0.0.1', debug=True)
