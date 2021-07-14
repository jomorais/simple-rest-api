#!/usr/bin/python
__author__ = 'joaci'
import os

from database.model import *


class Db:
    def __init__(self):
        self.init()

    @staticmethod
    def init():
        if Device.table_exists() is False:
            Device.create_table()
            return True
        else:
            return False

    @staticmethod
    def register_device(serial_number: str):
        try:
            new_device = Device(serial_number=serial_number)
            new_device.save()
            return REGISTER_DEVICE_SUCCESS, new_device
        except DatabaseError as ex:
            print('register_device::DatabaseError: %s' % ex)
            if 'UNIQUE constraint failed' in str(ex):
                return REGISTER_DEVICE_ALREADY_REGISTERED, None
        return REGISTER_DEVICE_ERROR, None

    @staticmethod
    def query_device(serial_number: str):
        try:
            for device in Device.select().where(Device.serial_number == serial_number).iterator():
                return QUERY_DEVICE_SUCCESS, device
            return QUERY_DEVICE_NOT_FOUND, None
        except DatabaseError as ex:
            print('query_device::DatabaseError: %s' % ex)
            return QUERY_DEVICE_ERROR, None

    @staticmethod
    def update_device_installation(device: Device, installation_address):
        if device.installation_status == Device.WAIT_FOR_INSTALLATION:
            device.installation_address = installation_address
            device.installation_status = Device.INSTALLED_DEVICE
            try:
                Device.update(installation_address=device.installation_address,
                              installation_status=device.installation_status)\
                    .where(Device.serial_number == device.serial_number).execute()
                return INSTALL_DEVICE_SUCCESS, device
            except DatabaseError as ex:
                print(ex)
                return INSTALL_DEVICE_ERROR, None
        else:
            return INSTALL_DEVICE_ALREADY_INSTALLED, None

    def install_device(self, serial_number: str, installation_address: str):

        status, device = self.query_device(serial_number=serial_number)

        if status == QUERY_DEVICE_NOT_FOUND:
            return INSTALL_DEVICE_NOT_FOUND, None

        if status == QUERY_DEVICE_SUCCESS:
            return self.update_device_installation(device=device, installation_address=installation_address)

    @staticmethod
    def delete_device(device: Device):
        try:
            device.delete().execute()
            return DELETE_DEVICE_SUCCESS, device
        except DatabaseError as ex:
            print(ex)
            return DELETE_DEVICE_ERROR, None

    def unregister_device(self, serial_number: str):

        status, device = self.query_device(serial_number=serial_number)

        if status == QUERY_DEVICE_ERROR:
            return DELETE_DEVICE_ERROR, None

        if status == QUERY_DEVICE_NOT_FOUND:
            return DELETE_DEVICE_NOT_FOUND, None

        if status == QUERY_DEVICE_SUCCESS:
            return self.delete_device(device)




