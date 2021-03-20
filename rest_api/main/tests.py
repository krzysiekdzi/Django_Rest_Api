import pymongo

from .handler import RequestsHandler


class CarsApiTests:
    def __init__(self):
        self.handler = RequestsHandler('mongodb://localhost:27017',
                                       'Cars_API_TEST_DB',
                                       'cars')

    def test_insert_car_handler(self):
        self.handler.insert_car_handler('Ford', "Mustang")

        result = self.handler.col.find_one({'make_name': 'Ford', 'model_name': 'Mustang'})
        assert result != None, 'insert_car_handler failed'

    def test_fetch_cars_handler(self):
        self.golf_id = self.handler.insert_car_handler('Volkswagen', 'Golf')['id']

        result = self.handler.fetch_cars_handler()
        assert type(result) == list and len(result) == 2, 'fetch_cars_handler failed'
    
    def test_insert_rate_handler(self):
        self.handler.insert_car_rate_handler(self.golf_id, 5)

        result = self.handler.col.find_one({'model_name': 'Golf'})
        assert result['rates'] and result['rates'][0] == 5, 'insert_rate_handler failed'

    def test_fetch_popular_cars_handler(self):
        result = self.handler.fetch_popular_cars_handler()

        assert result[0]['rates_number'] > result[1]['rates_number'], 'fetch_popular_cars_handler failed'
    
    def test_delete_car_handler(self):
        self.handler.delete_car_handler(self.golf_id)

        result = self.handler.col.find_one({'model_name': 'Golf'})
        assert result is None

    def database_clean_up(self):
        self.handler.col.drop()

api_tests = CarsApiTests()
api_tests.test_insert_car_handler()
api_tests.test_fetch_cars_handler()
api_tests.test_insert_rate_handler()
api_tests.test_fetch_popular_cars_handler()
api_tests.test_delete_car_handler()
print("Testing finished!")
api_tests.database_clean_up()
