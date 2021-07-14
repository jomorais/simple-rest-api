# :desktop_computer: A Simple RestAPI

![test status](https://github.com/jomorais/simple-rest-api/actions/workflows/simple-rest-api-app.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/jomorais/simple-rest-api/badge.svg)](https://coveralls.io/github/jomorais/simple-rest-api?branch=main) 


For testing with Insomnia, load [test/Insomnia-test.json](https://raw.githubusercontent.com/jomorais/simple-rest-api/7963b13a9aa7939ca38d4ba7ea4d44dd5f1b1e84/test/Insomnia-test.json)
<br>
<br>

### Running this REST API
-  Optional requirements
```bash
# optional: install 'curl' to make requests through terminal
sudo apt install curl
```
- Install requirements and run
```bash
git clone https://github.com/jomorais/simple-rest-api.git
```
```bash
cd simple-rest-api
chmod +x build_and_run.sh
./build_and_run.sh
```
<br>

### Registering new devices

:fast_forward: send a POST request to http://localhost:8989/register_device with a json payload like this:

```json
{
    "serial_number": "123456789"
}
```

- curl command:

```bash
  curl --header "Content-Type: application/json" --request POST --data '{"serial_number": "123456789"}' http://localhost:8989/register_device
```

:rewind: when is a success registering:
```json
{
    "data": {
        "created_at": "2021-07-11 13:58:20",
        "id": 1,
        "installation_address": "",
        "installation_status": 0,
        "serial_number": "123456789"
    },
    "status": "OK"
}
```
      
:rewind: when is already a device with this serial_number:
  
```json
{
    "data": "device already registered with this serial",
    "status": "FAIL"
}
```
<br>

### Query a device
- send a GET request to http://localhost:8989/query_device with a json payload like this: 
    
```json
{
    "serial_number": "123456789"
}
```
  
- curl command:

```bash
  curl --header "Content-Type: application/json" --request GET --data '{"serial_number": "123456789"}' http://localhost:8989/query_device
```

- when device was query successfully:

```json
{
    "data": {
        "created_at": "2021-07-11 13:58:20",
        "id": 1,
        "installation_address": "",
        "installation_status": 0,
        "serial_number": "123456789"
    },
    "status": "OK"
}
```
    
- when there is no device registered with the serial_number entered:

```json
{
    "data": "device was not found",
    "status": "FAIL"
}
```
<br>

### Install a registered device:

- send a POST request to http://localhost:8989/install_device with a json payload like this:
    
```json
{
    "serial_number": "123456789",
    "installation_address": "Rua D16, N55 Japiim Manaus/AM"
}
```
  
- curl command:
  
```bash
  curl --header "Content-Type: application/json" --request POST --data '{"serial_number": "123456789", "installation_address": "Rua D16, N55 Japiim Manaus/AM"}' http://localhost:8989/install_device
```

- when the installation was successfully:
```json
{
    "data": {
        "created_at": "2021-07-11 13:58:20",
        "id": 1,
        "installation_address": "Rua D16, N55 Japiim Manaus/AM",
        "installation_status": 1,
        "serial_number": "123456789"
    },
    "status": "OK"
}
```
    
- when there not any device registered with this serial number:

```json
{
    "data": "device was not found",
    "status": "FAIL"
}
```
  
- when the device already was installed:
```json
{
    "data": "device is already installed",
    "status": "FAIL"
}
```
<br>
  
### Unregister a device:

- send a DELETE request to http://localhost:8989/unregister_device with a json payload like this:
```json
{
    "serial_number": "123456789"
}
```
  
- curl command:
```bash
  curl --header "Content-Type: application/json" --request DELETE --data '{"serial_number": "123456789"}' http://localhost:8989/unregister_device
```

- when the device successfully unregistered:

```json
{
    "data": {
        "created_at": "2021-07-11 13:58:20",
        "id": 1,
        "installation_address": "Rua D16, N55 Japiim Manaus/AM",
        "installation_status": 1,
        "serial_number": "123456789"
    },
    "status": "OK"
}
```
  
- when there not any device registered with this serial number:

```json
{
    "data": "device was not found",
    "status": "FAIL"
}
```
