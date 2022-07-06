from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class UrlMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=16, message='Максимальная длинна ссылки 16 символов'),
                    Regexp(regex=r'^[a-zA-Z|\d]*$',
                           message='Указано недопустимое имя для короткой ссылки'),
                    Optional()]
    )
    submit = SubmitField('Создать')
