from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, IntegerField, \
    SelectField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    age = IntegerField('Возраст пользователя', validators=[DataRequired()])
    position = StringField('Сфера деятельности', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = EmailField('Адрес', validators=[DataRequired()])
    city = EmailField('Город проживания', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль',
                                   validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class JobsForm(FlaskForm):
    job = StringField('Название')
    team_leader = IntegerField("id teamleader")
    work_size = IntegerField("Время работы")
    collaborators = StringField("Участники")
    hazard_level = SelectField(
        "Уровень опасности",
        choices=[
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
        ],
    )
    is_finished = BooleanField('Завершена')
    submit = SubmitField('Применить')


class DepartmentsForm(FlaskForm):
    title = StringField('Название')
    chief = IntegerField("Chef id")
    members = StringField("Участники")
    email = EmailField("Почта", validators=[DataRequired()])
    submit = SubmitField('Применить')
