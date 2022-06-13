from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class UrlMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки', 
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 16, message='Максимальная длинна ссылки 16 символов'),
                    Optional()]
    )
    submit = SubmitField('Создать')
