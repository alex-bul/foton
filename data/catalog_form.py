# from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired

# images = UploadSet('images', IMAGES)


def get_catalog_form(form_value):
    class CatalogForm(FlaskForm):
        submit = SubmitField('Старт')

    for i, value in enumerate(form_value):
        setattr(CatalogForm, f'file{i}', FileField(value, validators=[
            FileRequired(),
            FileAllowed(['jpg', 'png'], 'Images only!')
        ]))

    return CatalogForm
