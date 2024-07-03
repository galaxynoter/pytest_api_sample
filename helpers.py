from jsonschema import validate as validate_json, ValidationError
import requests as r
from configKey import *
import time

today = time.strftime("%Y-%m-%d", time.localtime())

def validate_schema(response, schema):
    try:
        validate_json(response, schema)
    except ValidationError as e:
        print(e)
        return False
    return True

def update_headers():
    """Обновить токены"""
    try:
        response = r.get(url=auth_url, headers=headers, verify=False)
        headers['Authorization'] = response.json()['token']
    except:
        return False
    return True

