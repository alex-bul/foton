HOST = '127.0.0.2'
PORT = 8080
STATIC_FOLDER = 'static'
USER_PHOTOS_FOLDER = 'user_photos'
RESULT_PHOTOS_FOLDER = 'result_photos'
DEVELOPMENT = True   # включение режима разработки позволяет видеть обработчики, созданные администраторами

UPLOAD_PATH = f'{STATIC_FOLDER}/{USER_PHOTOS_FOLDER}'
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
]
# prepare catalog
