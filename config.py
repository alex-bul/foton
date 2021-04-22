HOST = '127.0.0.2'
PORT = 8080
STATIC_FOLDER = 'static'
USER_PHOTOS_FOLDER = 'user_photos'
UPLOAD_FOLDER = f'{STATIC_FOLDER}/{USER_PHOTOS_FOLDER}'
DB_FILE = "db/data.db"

catalog = [
    {
        'title': "Портрет",
        'description': "Создает уникальный портрет с вашим лицом. <br><b>Ван Гог</b> обзавидуется",
        'icon': "img/portrait.svg",
        'form_value': ['Загрузите фото человека'],
    },
    {
        'title': "Комикс",
        'description': "Ваше фото переносится в стиль комикса, сохраняя все детали исходного изображения",
        'icon': "img/comics.svg",
        'form_value': ['Загрузите фото человека']
    },
    # {
    #     'title': "Замена лиц",
    #     'description': "Алгоритм берет лицо с одного человека и накладывает на другого",
    #     'icon': "img/face.svg",
    #     'form_value': ['Загрузите фото человека (у него берется лицо)', 'Загрузите фото человека (ему меняется лицо)'],
    # },
]
