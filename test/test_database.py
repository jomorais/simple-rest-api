#!/usr/bin/python
__author__ = 'joaci'
import os
from database.db import Db
from database.model import *

models = [Device]

# db instance
urdb = Db()


def test_register_device():
    serial_number = "123456789"

    def setup():
        db.drop_tables(models)
        db.create_tables(models)
    setup()

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


def test_query_device():
    serial_number = "123456789"

    def setup_0():
        db.drop_tables(models)
        db.create_tables(models)
        urdb.register_device(serial_number=serial_number)
    setup_0()

    # test query device
    status, device = urdb.query_device(serial_number=serial_number)
    assert status == QUERY_DEVICE_SUCCESS
    assert device.id > 0
    assert device.serial_number == serial_number
    assert device.installation_address == ""
    assert device.installation_status == Device.WAIT_FOR_INSTALLATION

    def setup_1():
        db.drop_tables(models)
        db.create_tables(models)
    setup_1()

    # test query device not found
    status, device = urdb.query_device(serial_number=serial_number)
    assert status == QUERY_DEVICE_NOT_FOUND
    assert device is None


def test_update_device_instalation():
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

    def setup_1():
        db.drop_tables(models)
        db.create_tables(models)
        status, dev = urdb.register_device(serial_number=serial_number)
        dev.installation_status = Device.INSTALLED_DEVICE
        return status, dev
    status, dev = setup_1()

    status, device = urdb.update_device_installation(device=dev, installation_address=installation_address)
    assert status == INSTALL_DEVICE_ALREADY_INSTALLED
    assert device is None


def test_install_device():
    serial_number = "123456789"
    installation_address = "Rua D16 N55, Japiim"

    def setup_0():
        db.drop_tables(models)
        db.create_tables(models)
    setup_0()

    # test install device not found
    status, device = urdb.install_device(serial_number=serial_number, installation_address=installation_address)
    assert status == INSTALL_DEVICE_NOT_FOUND
    assert device is None

    def setup_1():
        db.drop_tables(models)
        db.create_tables(models)
        urdb.register_device(serial_number=serial_number)
    setup_1()

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


def test_delete_device():
    serial_number = "123456789"

    def setup_0():
        db.drop_tables(models)
        db.create_tables(models)
        urdb.register_device(serial_number=serial_number)
    setup_0()

    # test delete device
    status, device = urdb.delete_device(serial_number=serial_number)
    assert status == DELETE_DEVICE_SUCCESS
    assert device.id > 0
    assert device.serial_number == serial_number

    def setup_1():
        db.drop_tables(models)
        db.create_tables(models)
    setup_1()

    # test query device not found
    status, device = urdb.delete_device(serial_number=serial_number)
    assert status == DELETE_DEVICE_NOT_FOUND
    assert device is None

