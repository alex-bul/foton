HOST = '127.0.0.2'
PORT = 8080
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'user_photos'


catalog = [
    {
        'title': "Замена лиц",
        'description': "Алгоритм берет лицо с одного человека и накладывает на другого",
        'icon': "img/face.svg",
        'form_value': []
    },
    {
        'title': "Портрет",
        'description': "Создает уникальный портрет с вашим лицом. <br><b>Ван Гог</b> обзавидуется",
        'icon': "img/portrait.svg",
        'form_value': ['Загрузите фото человека'],
        'url': 'fddd'
    },
    {
        'title': "Комикс",
        'description': "Ваше фото переносится в стиль комикса, сохраняя все детали исходного изображения",
        'icon': "img/comics.svg",
        'form_value': ['Загрузите фото человека']
    }
]
