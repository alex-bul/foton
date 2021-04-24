import json

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


class CatalogPageForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    icon = FileField("Иконка (ТОЛЬКО SVG)", validators=[
        FileRequired(),
        FileAllowed(['svg'], 'Svg only!')
    ])
    url = StringField('Ссылка для запроса', validators=[DataRequired()])
    request_data = StringField(
        'Тело JSON запроса и headers при необходимости. На месте, где должен находится контент изображения должно быть "photo_field_foton" (ОБЯЗАТЕЛЬНО В КАВЫЧКАХ)',
        validators=[DataRequired()],
        render_kw={
            "placeholder": '{"data": {"file": "photo_field_foton", "another": "text"}, "headers": {"content-type": "application/json"}}'})
    request_photo_type = StringField(
        'В каком формате отправлять фото в запросе: binary или base64. Тип binary будет отправлен в поле для файлов, а base64 в теле пост запроса',
        validators=[DataRequired()],
        render_kw={"placeholder": 'base64,binary,base64'})
    result_key = StringField('Ключ, в котором будет содержаться результат в формате base64', validators=[DataRequired()])
    form_value = StringField('Описание к загрузке фото в форме (массив)', validators=[DataRequired()],
                             render_kw={"placeholder": '["Фото человека с лицом"]'})
    submit = SubmitField('Создать')

    @staticmethod
    def validate_request_data(form, field):
        try:
            print(field.data)
            request_data = json.loads(field.data)
        except json.decoder.JSONDecodeError:
            raise ValueError("Неккоректный JSON. Проверьте начилие фигурных скобок и отсутсвие одинарных кавычек")

        if 'data' not in request_data:
            raise ValueError('"data" обязательный параметр!')

        form.request_data.data = json.dumps(request_data)
