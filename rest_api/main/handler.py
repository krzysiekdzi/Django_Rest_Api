import pymongo
import json
import requests


from .utils import (
    integer_to_object_id,
    object_id_to_integer,
    check_model_in_external_API
)

class RequestsHandler:
    def __init__(self, host, database_name, collection_name):
        self.client = pymongo.MongoClient(host)
        self.database = self.client[database_name]
        self.col = self.database[collection_name]

    def insert_car_handler(self, make, model):
        if not make or not model:
            return 'Invalid car data'

        if not check_model_in_external_API(make, model):
            return f'Model not found in {make} models list'
        
        db_record = self.col.find_one({'model_name': model})
        if db_record:
            return f'{model} already present in database!'
        insertion_result = self.col.insert({'model_name': model, 'make_name': make, 'rates': []})

        return {'id': object_id_to_integer(insertion_result)}


    def fetch_cars_handler(self):
        cars_list = []
        for car in self.col.find({}):
            cars_list.append({
                'id': object_id_to_integer(car['_id']),
                'make': car['make_name'],
                'model': car['model_name'],
                'avg_rating': sum(car['rates'])/len(car['rates']) if car['rates'] else 0
            })
        return cars_list


    def fetch_popular_cars_handler(self):
        cars_list = []
        for car in self.col.find({}):
            cars_list.append({
                'id': object_id_to_integer(car['_id']),
                'make': car['make_name'],
                'model': car['model_name'],
                'rates_number': len(car['rates'])
            })
        cars_list.sort(key=lambda car_dict: car_dict['rates_number'], reverse=True)
        return cars_list


    def delete_car_handler(self, car_id):
        res = self.col.delete_one({'_id': integer_to_object_id(int(car_id))})

        if res.deleted_count > 0:
            return True
        return f'Object with id {car_id} not found'


    def insert_car_rate_handler(self, integer_id, rate):
        if rate < 1 or rate > 5:
            return 'Invalid rate value (1 to 5)'

        car_id = integer_to_object_id(integer_id)
        db_record = self.col.find_one({'_id': car_id})
        if not db_record:
            return 'Car not found in database'

        db_record['rates'].append(rate)
        self.col.update_one({'_id': car_id}, {'$set': {'rates': db_record['rates']}})
        return True
