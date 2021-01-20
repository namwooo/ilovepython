from unittest import mock
from unittest.mock import Mock, patch

import pytest
import requests
from requests import Response, HTTPError, ConnectionError

# from config import HOST_URL
from config import HOST_URL


class Grade:
    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Trait:
    courage_grade = Grade()
    integrity_grade = Grade()
    grace_grade = Grade()

    def __init__(self, name):
        self.name = name
        self.reported = False

    @property
    def total(self):
        return self.courage_grade + self.integrity_grade + self.grace_grade

    @property
    def average(self):
        return self.total / 3

    @property
    def report_payload(self):
        return {
            'total': self.total,
            'average': self.average,
            'courage_grade': self.courage_grade,
            'integrity_grade': self.integrity_grade,
            'grace_grade': self.grace_grade
        }

    def report(self):
        try:
            response = requests.post(HOST_URL, data=self.report_payload)
        except ConnectionError:
            raise ValueError('report failed')

        response.raise_for_status()

        self.reported = True

        return response


@pytest.fixture
def trait():
    trait = Trait(name='남우')
    trait.courage_grade = 90
    trait.integrity_grade = 90
    trait.grace_grade = 90
    return trait


@pytest.fixture
def response_200():
    response = Response()
    response.status_code = 200
    return response


@pytest.fixture
def response_500():
    response = Response()
    response.status_code = 500
    return response


# def test_trait_report_200(trait, response_200):
#     with mock.patch('requests.post', return_value=response_200):
#         response = trait.report()
#         assert True is trait.reported
#
#
# def test_trait_report_500(trait, response_500):
#     with mock.patch('requests.post', return_value=response_500):
#         with pytest.raises(HTTPError):
#             response = trait.report()
#         assert False is trait.reported

#
# def test_trait_report_connection_error(trait):
#     with mock.patch('requests.post', side_effect=ConnectionError):
#         with pytest.raises(ValueError):
#             response = trait.report()


# @patch('requests.post')
# def test_trait_report_200(mock_post, trait, response_200):
#     mock_post.return_value = response_200
#     response = trait.report()
#     assert True is trait.reported
#
#
# @patch('requests.post')
# def test_trait_report_500(mock_post, trait, response_500):
#     mock_post.return_value = response_500
#     with pytest.raises(HTTPError):
#         response = trait.report()
#     assert False is trait.reported
#
#
# @patch('requests.post')
# def test_trait_report_connection_error(mock_post, trait):
#     mock_post.side_effect = ConnectionError
#     with pytest.raises(ValueError):
#         response = trait.report()

# # patch location
# @patch(f'{__name__}.HOST_URL', 'http://aimmo2.co.kr')
# def test_trait_report_200(trait):
#     with pytest.raises(ValueError):
#         response = trait.report()



if __name__ == '__main__':
    # spec & spec_set
    # trait_mock = Mock(spec=Trait(name='남우'))
    trait_mock = Mock(spec_set=Trait(name='남우'))


    def mocked():
        print('you are mocked')


    trait_mock.mocked = mocked
