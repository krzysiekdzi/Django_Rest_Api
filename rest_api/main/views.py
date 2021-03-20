import json
from bson.objectid import ObjectId
from django.http import HttpResponse, JsonResponse

from .handler import RequestsHandler
from .utils import add_charset_header


handler = RequestsHandler(host='mongodb://mongo:27017',
                          database_name='Cars_API',
                          collection_name='cars')


def cars_request_router(request):
    routes = {
        'POST': insert_car_endpoint,
        'GET': fetch_cars_endpoint
    }
    if request.method not in routes:
        return HttpResponse('Invalid request type!', status=404)
    return routes[request.method](request)


def response_mapper(func):
    def mapping(*args, **kwargs):
        result = func(*args, **kwargs)
        if type(result) == list or type(result) == dict:
            return add_charset_header(JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False}))
        elif result is True:
            return HttpResponse(status=200)
        else:
            return HttpResponse(result, status=500)
    return mapping

#ENDPOINTS
@response_mapper
def insert_car_endpoint(request):
    raw_body = request.body.decode('utf-8')
    body = json.loads(raw_body)
    return handler.insert_car_handler(body['make'].capitalize(), body['model'].capitalize())


@response_mapper
def fetch_cars_endpoint(request):
    return handler.fetch_cars_handler()


@response_mapper
def fetch_popular_cars_endpoint(request):
    return handler.fetch_popular_cars_handler()


@response_mapper
def delete_car_endpoint(request, car_id):
    if request.method != 'DELETE':
        return HttpResponse('Invalid request type', status=404)
    return handler.delete_car_handler(car_id)


@response_mapper
def insert_car_rate_endpoint(request):
    raw_body = request.body.decode('utf-8')
    body = json.loads(raw_body)
    return handler.insert_car_rate_handler(body['car_id'], body['rating'])
