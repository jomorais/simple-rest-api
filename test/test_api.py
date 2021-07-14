#!/usr/bin/python
__author__ = 'joaci'
import os

import pytest

from api.api import Api
from database.model import *
from unittest.mock import patch

models = [Device]

api = Api()


def clear_database():
    db.drop_tables(models)
    db.create_tables(models)


def test_register_device_success():
    parameters = {'serial_number': '123456789'}

    def setup():
        clear_database()
    setup()

    result = api.register_device(parameters)
    assert result['status'] == 'OK'
    assert result['data']['id'] == 1
    assert result['data']['serial_number'] == parameters['serial_number']
    # assert result['data']['created_at'] == datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert result['data']['installation_address'] == ""
    assert result['data']['installation_status'] == Device.WAIT_FOR_INSTALLATION


def test_register_device_already_registered():
    parameters = {'serial_number': '123456789'}

    def setup():
        clear_database()
        api.register_device(parameters)
    setup()

    result = api.register_device(parameters)
    assert result['status'] == 'FAIL'
    assert result['data'] == "device already registered with this serial"


def test_register_device_key_serial_number():
    parameters = {}

    def setup():
        clear_database()
    setup()

    result = api.register_device(parameters)
    assert result['status'] == 'FAIL'
    assert result['data'] == "the key 'serial_number' not found on post parameter"


def test_register_device_error():
    parameters = {'serial_number': '123456789'}

    with patch('database.db.Db.register_device', return_value=(REGISTER_DEVICE_ERROR, None)):
        result = api.register_device(parameters)
        assert result['status'] == 'FAIL'
        assert result['data'] == "register_device error"


def test_unregister_device_success():
    parameters = {'serial_number': '123456789'}

    def setup():
        clear_database()
        api.register_device(parameters)
    setup()

    result = api.unregister_device(parameters)
    assert result['status'] == 'OK'
    assert result['data']['id'] == 1
    assert result['data']['serial_number'] == parameters['serial_number']
    # assert result['data']['created_at'] == datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert result['data']['installation_address'] == ""
    assert result['data']['installation_status'] == Device.WAIT_FOR_INSTALLATION


def test_unregister_device_key_serial_number():
    parameters = {}

    result = api.unregister_device(parameters)
    assert result['status'] == 'FAIL'
    assert result['data'] == "the key 'serial_number' not found on post parameter"


def test_unregister_device_not_found():
    parameters = {'serial_number': '123456789'}

    def setup():
        clear_database()
    setup()

    # test delete_device not found
    result = api.unregister_device(parameters)
    assert result['status'] == 'FAIL'
    assert result['data'] == "device was not found"


def test_unregister_device_error():
    parameters = {'serial_number': '123456789'}

    with patch('database.db.Db.unregister_device', return_value=(DELETE_DEVICE_ERROR, None)):
        result = api.unregister_device(parameters)
        assert result['status'] == 'FAIL'
        assert result['data'] == "unregister_device error"


def test_query_device_success():
    parameters = {'serial_number': '123456789'}

    def setup():
        clear_database()
        api.register_device(parameters)
    setup()

    # test query_device success
    result = api.query_device(parameters)
    assert result['status'] == 'OK'
    assert result['data']['id'] == 1
    assert result['data']['serial_number'] == parameters['serial_number']
    # assert result['data']['created_at'] == datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert result['data']['installation_address'] == ""
    assert result['data']['installation_status'] == Device.WAIT_FOR_INSTALLATION


def test_query_device_key_serial_number():
    parameters = {}
    # test parameter key
    result = api.query_device(parameters)
    assert result['status'] == 'FAIL'
    assert result['data'] == "the key 'serial_number' not found on post parameter"


def test_query_device_not_found():
    parameters = {'serial_number': '123456789'}

    def setup():
        clear_database()
    setup()

    # test query_device not found
    result = api.query_device(parameters)
    assert result['status'] == 'FAIL'
    assert result['data'] == "device was not found"


def test_query_device_error():
    parameters = {'serial_number': '123456789'}

    with patch('database.db.Db.query_device', return_value=(QUERY_DEVICE_ERROR, None)):
        result = api.query_device(parameters)
        assert result['status'] == 'FAIL'
        assert result['data'] == "query_device error"


def test_install_device_success():
    parameters = {'serial_number': '123456789', 'installation_address': 'Rua d16 N55, Japiim Manaus/AM'}

    def setup():
        clear_database()
        api.register_device(parameters)

    setup()

    # test parameter key
    result = api.install_device(parameters)
    assert result['status'] == 'OK'
    assert result['data']['id'] == 1
    assert result['data']['serial_number'] == parameters['serial_number']
    assert result['data']['installation_address'] == "Rua d16 N55, Japiim Manaus/AM"
    assert result['data']['installation_status'] == Device.INSTALLED_DEVICE


def test_install_device_key_serial_number_or_installation_address():
    parameters = {}

    # test parameter key
    result = api.install_device(parameters)
    assert result['status'] == 'FAIL'
    assert result['data'] == "any of this keys ['serial_number', 'installation_address'] was not found on post parameter"


def test_install_device_not_found():
    parameters = {'serial_number': '123456789', 'installation_address': 'Rua d16 N55, Japiim Manaus/AM'}

    def setup_1():
        clear_database()

    setup_1()

    # test install_device not found
    result = api.install_device(parameters)
    assert result['status'] == 'FAIL'
    assert result['data'] == "device was not found"


def test_install_device_already_installed():
    parameters = {'serial_number': '123456789', 'installation_address': 'Rua d16 N55, Japiim Manaus/AM'}

    def setup():
        clear_database()
        api.register_device(parameters)
        api.install_device(parameters)
    setup()

    # test parameter key
    result = api.install_device(parameters)
    assert result['status'] == 'FAIL'
    assert result['data'] == "device is already installed"


def test_install_device_error():
    parameters = {'serial_number': '123456789', 'installation_address': 'Rua d16 N55, Japiim Manaus/AM'}

    with patch('database.db.Db.install_device', return_value=(INSTALL_DEVICE_ERROR, None)):
        result = api.install_device(parameters)
        assert result['status'] == 'FAIL'
        assert result['data'] == "install_device error"
