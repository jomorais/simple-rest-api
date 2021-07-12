#!/usr/bin/python
__author__ = 'joaci'

from database.model import *
from database.db import Db
from utils.utils import *

SERIAL_NUMBER_NOT_FOUND = -1


class Api:

    def __init__(self):
        self.database = Db()

    def register_device(self, parameters: dict):
        result = dict()
        if key_checker(['serial_number'], parameters) is False:
            result['status'] = 'FAIL'
            result['data'] = "the key 'serial_number' not found on post parameter"
            return result

        # register a device
        status, registered_device = self.database.register_device(serial_number=parameters['serial_number'])

        if status == REGISTER_DEVICE_SUCCESS:
            result['status'] = 'OK'
            result['data'] = registered_device.to_dict()
            return result
        elif status == REGISTER_DEVICE_ALREADY_REGISTERED:
            result['status'] = 'FAIL'
            result['data'] = "device already registered with this serial"
            return result

        result['status'] = 'FAIL'
        result['data'] = "register_device error"
        return result

    def query_device(self, parameters: dict):
        result = dict()
        if key_checker(['serial_number'], parameters) is False:
            result['status'] = 'FAIL'
            result['data'] = "the key 'serial_number' not found on post parameter"
            return result

        # query a device
        status, device = self.database.query_device(serial_number=parameters['serial_number'])

        if status == QUERY_DEVICE_SUCCESS:
            result['status'] = 'OK'
            result['data'] = device.to_dict()
            return result
        elif status == QUERY_DEVICE_NOT_FOUND:
            result['status'] = 'FAIL'
            result['data'] = "device was not found"
            return result

        result['status'] = 'FAIL'
        result['data'] = "query_device error"
        return result

    def install_device(self, parameters: dict):
        result = dict()
        keys = ['serial_number', 'installation_address']
        if key_checker(keys, parameters) is False:
            result['status'] = 'FAIL'
            result['data'] = "any of this keys %s was not found on post parameter" % keys
            return result

        # install a device
        status, installed_device = self.database.install_device(serial_number=parameters['serial_number'],
                                                                installation_address=parameters['installation_address'])
        if status == INSTALL_DEVICE_SUCCESS:
            result['status'] = 'OK'
            result['data'] = installed_device.to_dict()
            return result
        elif status == INSTALL_DEVICE_NOT_FOUND:
            result['status'] = 'FAIL'
            result['data'] = "device was not found"
            return result
        elif status == INSTALL_DEVICE_ALREADY_INSTALLED:
            result['status'] = 'FAIL'
            result['data'] = "device is already installed"
            return result

        result['status'] = 'FAIL'
        result['data'] = "install_device error"
        return result

    def delete_device(self, parameters: dict):
        result = dict()
        if key_checker(['serial_number'], parameters) is False:
            result['status'] = 'FAIL'
            result['data'] = "the key 'serial_number' not found on post parameter"
            return result

        # delete a device
        status, deleted_device = self.database.delete_device(serial_number=parameters['serial_number'])

        if status == DELETE_DEVICE_SUCCESS:
            result['status'] = 'OK'
            result['data'] = deleted_device.to_dict()
            return result
        elif status == DELETE_DEVICE_NOT_FOUND:
            result['status'] = 'FAIL'
            result['data'] = "device was not found"
            return result

        result['status'] = 'FAIL'
        result['data'] = "delete_device error"
        return result

