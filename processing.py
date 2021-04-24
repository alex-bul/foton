import sqlite3
import time
import json
import datetime
import base64
import requests

from data import db_session
from generate_catalog import get_catalog
from werkzeug.utils import secure_filename
from process_utils.conventers import conventers
from config import RESULT_PHOTOS_FOLDER, DB_FILE


def find_and_replace(d, data_replace):
    for key, val in d.items():
        if isinstance(val, dict):
            find_and_replace(val, data_replace)
        else:
            if val == 'image':
                d[key] = data_replace.pop(0)
    return d


def process_by_url(url, request_data, request_photo_type, result_key, photos):
    payload, headers = request_data['data'], request_data['headers']
    data_replace = []
    for photo in photos:
        if request_photo_type == 'binary':
            data_replace.append(open(photo, "rb"))
        else:
            data_replace.append(base64.standard_b64encode(open(photo, "rb").read()))
    payload = find_and_replace(payload, data_replace)
    res = requests.post(url, data=payload, headers=headers).json()[result_key]
    return base64.decodebytes(str.encode(res))


def main():
    db_session.global_init(DB_FILE)
    conn = sqlite3.connect(DB_FILE, isolation_level=None)
    conn.execute('pragma journal_mode=wal')
    c = conn.cursor()
    while True:
        try:
            catalog = get_catalog()
            orders = c.execute("SELECT id, catalog_id, request_data FROM processes WHERE is_finished == 0").fetchall()
            for i, catalog_id, request_data in orders:
                try:
                    if 'url' in catalog[catalog_id]:
                        catalog_obj = catalog[catalog_id]
                        content = process_by_url(catalog_obj['url'], catalog_obj['request_data'],
                                       catalog_obj['request_photo_type'], catalog_obj['result_key'], json.loads(request_data))
                    else:
                        func = conventers[catalog_id]
                        content = func(json.loads(request_data))
                    filename = f"{RESULT_PHOTOS_FOLDER}/{secure_filename(f'{datetime.datetime.now()}.jpg')}"
                    with open('static/' + filename, "wb") as f:
                        f.write(content)
                    c.execute(f"UPDATE processes SET is_finished = ?, result_code = ?, result = ? WHERE id = ?",
                              (True, 200, filename, i))
                except KeyError:
                    c.execute(f"UPDATE processes SET is_finished = ?, result_code = ?, result = ? WHERE id = ?",
                              (True, 400, "Неправильный ключ для результата запроса", i))
                except Exception as ex:
                    c.execute(f"UPDATE processes SET is_finished = ?, result_code = ?, result = ? WHERE id = ?",
                              (True, 400, str(ex), i))
            time.sleep(1)
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    main()
