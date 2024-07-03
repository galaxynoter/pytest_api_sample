import pytest
import requests as r
from configKey import *
from schemas.schemas_valid import *
from helpers import *

class TestClass:
    """Классовые переменные с динамическими данными"""
    specific_data = ''

    @classmethod
    def setup_class(cls):
        """Обновление токенов"""
        if not update_headers():
            pytest.exit('Ошибка получения токенов', 3)

    @classmethod
    def teardown_class(cls):
        """Удаление данных"""
        update_headers()
        if TestClass.specific_data:
            r.delete(f'{link}/***/{TestClass.specific_data}', headers=headers)

    def test_get(self):
        url = f'{link}/****'
        response = r.get(url, headers=headers)
        assert response.status_code == 200, f'Ожидался статус-код 200 OK, но получен {response.status_code}'
        assert validate_schema(response.json(), schema_get), 'Джейсон схема не соответствует'
        response = r.get(url, headers=headers_empty_token)
        assert response.status_code == 403, f"Ожидался статус-код 403 forbidden, но получен {response.status_code}"

    def test_post(self):
        url = f'{link}/****'
        response_data_should_be = {}
        payload = {}

        response = r.post(url, headers=headers, json=payload)
        assert response.status_code == 200, f'Ожидался статус-код 200 ОК, но получен {response.status_code} \n {response.text}'
        assert validate_schema(response.text, schema_post)
        assert (response_data_should_be in body for body in response.json())
        TestClass.specific_data = response.json()['specific_data']
        print('Получена информация specific_data ' + TestClass.specific_data)
