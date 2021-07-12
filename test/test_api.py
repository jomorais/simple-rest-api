#!/usr/bin/python
__author__ = 'joaci'
import os
from api.api import Api
from database.model import *

models = [Device]

api = Api()


def clear_database():
    db.drop_tables(models)
    db.create_tables(models)


def test_register_device():
    parameters = {'serial_number': '123456789'}

    def setup_0():
        clear_database()

    setup_0()

    result = api.register_device({})
    assert result['status'] == 'FAIL'
    assert result['data'] == "the key 'serial_number' not found on post parameter"

    result = api.register_device(parameters)
    assert result['status'] == 'OK'
    assert result['data']['id'] == 1
    assert result['data']['serial_number'] == parameters['serial_number']
    # assert result['data']['created_at'] == datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert result['data']['installation_address'] == ""
    assert result['data']['installation_status'] == Device.WAIT_FOR_INSTALLATION

    result = api.register_device(parameters)
    assert result['status'] == 'FAIL'
    assert result['data'] == "device already registered with this serial"


def test_delete_device():
    parameters = {'serial_number': '123456789'}

    def setup_0():
        clear_database()
        api.register_device(parameters)

    setup_0()

    result = api.delete_device({})
    assert result['status'] == 'FAIL'
    assert result['data'] == "the key 'serial_number' not found on post parameter"

    result = api.delete_device(parameters)
    assert result['status'] == 'OK'
    assert result['data']['id'] == 1
    assert result['data']['serial_number'] == parameters['serial_number']
    # assert result['data']['created_at'] == datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert result['data']['installation_address'] == ""
    assert result['data']['installation_status'] == Device.WAIT_FOR_INSTALLATION

    def setup_1():
        clear_database()
    setup_1()

    # test delete_device not found
    result = api.delete_device(parameters)
    assert result['status'] == 'FAIL'
    assert result['data'] == "device was not found"


def test_query_device():
    parameters = {'serial_number': '123456789'}

    def setup_0():
        clear_database()
        api.register_device(parameters)
    setup_0()

    # test parameter key
    result = api.query_device({})
    assert result['status'] == 'FAIL'
    assert result['data'] == "the key 'serial_number' not found on post parameter"

    # test query_device success
    result = api.query_device(parameters)
    assert result['status'] == 'OK'
    assert result['data']['id'] == 1
    assert result['data']['serial_number'] == parameters['serial_number']
    # assert result['data']['created_at'] == datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert result['data']['installation_address'] == ""
    assert result['data']['installation_status'] == Device.WAIT_FOR_INSTALLATION

    def setup_1():
        clear_database()
    setup_1()

    # test query_device not found
    result = api.query_device(parameters)
    assert result['status'] == 'FAIL'
    assert result['data'] == "device was not found"


def test_install_device():
    parameters = {'serial_number': '123456789', 'installation_address': 'Rua d16 N55, Japiim Manaus/AM'}

    def setup_0():
        clear_database()
        api.register_device(parameters)

    setup_0()

    # test parameter key
    result = api.install_device({})
    assert result['status'] == 'FAIL'
    assert result['data'] == "any of this keys ['serial_number', 'installation_address'] was not found on post parameter"

    # test parameter key
    result = api.install_device(parameters)
    assert result['status'] == 'OK'
    assert result['data']['id'] == 1
    assert result['data']['serial_number'] == parameters['serial_number']
    assert result['data']['installation_address'] == "Rua d16 N55, Japiim Manaus/AM"
    assert result['data']['installation_status'] == Device.INSTALLED_DEVICE

    result = api.install_device(parameters)
    assert result['status'] == 'FAIL'
    assert result['data'] == "device is already installed"

    def setup_1():
        clear_database()

    setup_1()

    # test install_device not found
    result = api.install_device(parameters)
    assert result['status'] == 'FAIL'
    assert result['data'] == "device was not found"
