import sqlite3
import time
import json
import datetime

from generate_catalog import get_catalog
from werkzeug.utils import secure_filename
from process_utils.conventers import conventers
from config import RESULT_PHOTOS_FOLDER, DB_FILE

def process_by_url(url, request_data, fields_types, photos):
    pass

def main():
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
                        process_by_url(catalog_obj['url'], catalog_obj['request_data'], catalog_obj['fields_types'], json.loads(request_data))
                    else:
                        func = conventers[catalog_id]
                        content = func(json.loads(request_data))
                        filename = f"{RESULT_PHOTOS_FOLDER}/{secure_filename(f'{datetime.datetime.now()}.jpg')}"
                        with open('static/' + filename, "wb") as f:
                            f.write(content)
                        c.execute(f"UPDATE processes SET is_finished = ?, result_code = ?, result = ? WHERE id = ?",
                                  (True, 200, filename, i))
                except Exception as ex:
                    c.execute(f"UPDATE processes SET is_finished = ?, result_code = ?, result = ? WHERE id = ?",
                              (True, 400, str(ex), i))
            time.sleep(1)
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    main()
