#!/usr/bin/python
__author__ = 'joaci'

from peewee import *
import datetime

database_file = 'simple-api-database.db'
db = SqliteDatabase(database_file)

SUCCESS = True
FAIL = False


DB_ERROR = -1
EXCEPTION = -2

REGISTER_DEVICE_SUCCESS = 0
REGISTER_DEVICE_ALREADY_REGISTERED = -1
REGISTER_DEVICE_ERROR = -2

QUERY_DEVICE_SUCCESS = 0
QUERY_DEVICE_NOT_FOUND = -1
QUERY_DEVICE_ERROR = -2

INSTALL_DEVICE_SUCCESS = 0
INSTALL_DEVICE_NOT_FOUND = -1
INSTALL_DEVICE_ERROR = -2
INSTALL_DEVICE_ALREADY_INSTALLED = -3

DELETE_DEVICE_SUCCESS = 0
DELETE_DEVICE_NOT_FOUND = -1
DELETE_DEVICE_ERROR = -2


class BaseModel(Model):
    class Meta:
        database = db


class Device(BaseModel):
    INSTALLED_DEVICE = 1
    WAIT_FOR_INSTALLATION = 0
    id = IntegerField(unique=True, index=True, primary_key=True)
    created_at = DateTimeField(index=True, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    serial_number = TextField(unique=True, index=True)
    installation_address = TextField(default="")
    installation_status = IntegerField(default=WAIT_FOR_INSTALLATION)

    def to_dict(self):
        device = dict()
        device['id'] = self.id
        device['created_at'] = self.created_at
        device['serial_number'] = self.serial_number
        device['installation_address'] = self.installation_address
        device['installation_status'] = self.installation_status
        return device
