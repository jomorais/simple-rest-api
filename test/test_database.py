#!/usr/bin/python
__author__ = 'joaci'
import os
from database.db import Db
from database.model import *
from unittest.mock import patch
from peewee import *
import pytest

models = [Device]

# db instance
urdb = Db()


def test_database_init():
    def setup_0():
        db.drop_tables(models)

    setup_0()

    status = urdb.init()
    assert status is True

    with patch('database.model.Device.create_table', side_effect=OperationalError):
        status = urdb.init()


def test_register_device():
    serial_number = "123456789"

    def setup_0():
        db.drop_tables(models)
        db.create_tables(models)
        print('setup_0')

    setup_0()

    # test save device
    status, device = urdb.register_device(serial_number=serial_number)
    assert status == REGISTER_DEVICE_SUCCESS
    assert device.id > 0
    assert device.serial_number == serial_number
    assert device.installation_address == ""
    assert device.installation_status == Device.WAIT_FOR_INSTALLATION

    # test save same device again
    status, device = urdb.register_device(serial_number=serial_number)
    assert status == REGISTER_DEVICE_ALREADY_REGISTERED
    assert device is None

    with patch('database.model.Device.save', side_effect=(DatabaseError())):
        status, device = urdb.register_device(serial_number=serial_number)


def test_query_device():
    serial_number = "123456789"

    def setup():
        db.drop_tables(models)
        db.create_tables(models)
        urdb.register_device(serial_number=serial_number)
    setup()

    # test query device
    status, device = urdb.query_device(serial_number=serial_number)
    assert status == QUERY_DEVICE_SUCCESS
    assert device.id > 0
    assert device.serial_number == serial_number
    assert device.installation_address == ""
    assert device.installation_status == Device.WAIT_FOR_INSTALLATION


def test_query_device_not_found():
    serial_number = "123456789"

    def setup():
        db.drop_tables(models)
        db.create_tables(models)
    setup()

    # test query device not found
    status, device = urdb.query_device(serial_number=serial_number)
    assert status == QUERY_DEVICE_NOT_FOUND
    assert device is None


def test_query_device_error():
    serial_number = "123456789"

    def setup():
        db.drop_tables(models)
    setup()

    status, device = urdb.query_device(serial_number=serial_number)
    assert status == QUERY_DEVICE_ERROR
    assert device is None


def test_update_device_installation_success():
    serial_number = "123456789"
    installation_address = "Rua D16 N55 Japiim Manaus/AM"

    def setup_0():
        db.drop_tables(models)
        db.create_tables(models)
        return urdb.register_device(serial_number=serial_number)
    status, dev = setup_0()

    # test update device installation success
    status, device = urdb.update_device_installation(device=dev, installation_address=installation_address)
    assert status == INSTALL_DEVICE_SUCCESS
    assert device.serial_number == serial_number
    assert device.installation_address == installation_address
    assert device.installation_status == Device.INSTALLED_DEVICE


def test_update_device_installation_already_installed():
    serial_number = "123456789"
    installation_address = "Rua D16 N55 Japiim Manaus/AM"

    def setup():
        db.drop_tables(models)
        db.create_tables(models)
        status, dev = urdb.register_device(serial_number=serial_number)
        dev.installation_status = Device.INSTALLED_DEVICE
        return status, dev
    status, dev = setup()

    status, device = urdb.update_device_installation(device=dev, installation_address=installation_address)
    assert status == INSTALL_DEVICE_ALREADY_INSTALLED
    assert device is None


def test_update_device_installation_error():
    installation_address = "Rua D16 N55 Japiim Manaus/AM"

    def setup():
        db.drop_tables(models)
        dev = Device()
        return dev
    dev = setup()

    status, device = urdb.update_device_installation(device=dev, installation_address=installation_address)
    assert status == INSTALL_DEVICE_ERROR
    assert device is None


def test_install_device_success():
    serial_number = "123456789"
    installation_address = "Rua D16 N55, Japiim"

    def setup():
        db.drop_tables(models)
        db.create_tables(models)
        urdb.register_device(serial_number=serial_number)
    setup()

    # test install device success
    status, device = urdb.install_device(serial_number=serial_number, installation_address=installation_address)
    assert status == INSTALL_DEVICE_SUCCESS
    assert device.serial_number == serial_number
    assert device.installation_address == installation_address
    assert device.installation_status == Device.INSTALLED_DEVICE

    # test install device success
    status, device = urdb.install_device(serial_number=serial_number, installation_address=installation_address)
    assert status == INSTALL_DEVICE_ALREADY_INSTALLED
    assert device is None


def test_install_device_not_found():
    serial_number = "123456789"
    installation_address = "Rua D16 N55, Japiim"

    def setup():
        db.drop_tables(models)
        db.create_tables(models)
    setup()

    # test install device not found
    status, device = urdb.install_device(serial_number=serial_number, installation_address=installation_address)
    assert status == INSTALL_DEVICE_NOT_FOUND
    assert device is None


def test_install_device_already_installed():
    serial_number = "123456789"
    installation_address = "Rua D16 N55, Japiim"

    def setup():
        db.drop_tables(models)
        db.create_tables(models)
        urdb.register_device(serial_number=serial_number)
        urdb.install_device(serial_number=serial_number, installation_address=installation_address)
    setup()

    # test install device success
    status, device = urdb.install_device(serial_number=serial_number, installation_address=installation_address)
    assert status == INSTALL_DEVICE_ALREADY_INSTALLED
    assert device is None


def test_delete_device_success():
    serial_number = "123456789"

    def setup():
        db.drop_tables(models)
        db.create_tables(models)
        return urdb.register_device(serial_number=serial_number)
    status, dev = setup()

    status, device = urdb.delete_device(dev)
    assert status == DELETE_DEVICE_SUCCESS
    assert device.id > 0
    assert device.serial_number == serial_number


def test_delete_device_fail():
    serial_number = "123456789"

    def setup():
        db.drop_tables(models)
        db.create_tables(models)
        sts, dev = urdb.register_device(serial_number=serial_number)
        db.drop_tables(models)
        return sts, dev
    status, dev = setup()

    status, device = urdb.delete_device(dev)
    assert status == DELETE_DEVICE_ERROR
    assert device is None


def test_unregister_device_success():
    serial_number = "123456789"

    def setup():
        db.drop_tables(models)
        db.create_tables(models)
        urdb.register_device(serial_number=serial_number)
    setup()

    # test delete device
    status, device = urdb.unregister_device(serial_number=serial_number)
    assert status == DELETE_DEVICE_SUCCESS
    assert device.id > 0
    assert device.serial_number == serial_number


def test_unregister_device_not_found():
    serial_number = "123456789"

    def setup():
        db.drop_tables(models)
        db.create_tables(models)
    setup()

    # test query device not found
    status, device = urdb.unregister_device(serial_number=serial_number)
    assert status == DELETE_DEVICE_NOT_FOUND
    assert device is None


def test_unregister_device_error():
    serial_number = "123456789"

    def setup():
        db.drop_tables(models)
        print('setup')
    setup()

    # test test_unregister_device_error
    print('exec')
    status, device = urdb.unregister_device(serial_number=serial_number)
    assert status == DELETE_DEVICE_ERROR
    assert device is None


