import json
from ast import literal_eval

from data import db_session
from data.catalog_page import CatalogPage
from config import catalog


def get_catalog():
    result = [] + catalog
    db_sess = db_session.create_session()

    catalog_pages = db_sess.query(CatalogPage).filter(CatalogPage.is_delete == 0).all()
    for page in catalog_pages:
        data = page.__dict__
        for i in list(filter(lambda x: x.startswith('_'), data.keys())):
            data.pop(i, None)
        data['form_value'] = literal_eval(data['form_value'])
        data['request_data'] = json.loads(data['request_data'])
        result.append(data)
    return result
