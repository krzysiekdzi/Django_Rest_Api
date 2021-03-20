import requests
from bson.objectid import ObjectId


def add_charset_header(response):
    old_header = response._headers['content-type']
    new_header = (old_header[0], old_header[1] + ';charset=UTF-8')
    response._headers['content-type'] = new_header
    return response


def integer_to_object_id(int_id):
    return  ObjectId(str(hex(int_id))[2:]) 


def object_id_to_integer(object_id):
    return int(str(object_id), 16)


def check_model_in_external_API(make, model):
    res = requests.get(f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make}?format=json')
    if res.status_code != 200:
        return False
    data = res.json()['Results']
    models = [data_record['Model_Name'].capitalize() for data_record in data]
    return True if model in models else False
