# RestAPI - Unidade Remota de Balanço Energético

## todo:
- testar parâmetro json do "request.json"

## CADASTRANDO NOVOS DEVICES:
- Enviar uma requisição POST para a URL: http://localhost:8989/register_device passando como parâmetro o json com o serial_number da unidade: 
    ```json
    {"serial_number": "123456789"}
    ```
- comando curl:
    ```bash
    curl --header "Content-Type: application/json" --request POST --data '{"serial_number": "123456789"}' http://localhost:8989/register_device
    ```
  
    ### RESPOSTA ESPERADA QUANDO:
    - CADASTRO FOR EFETUADO COM SUCESSO:
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
      
    - JÁ HOUVER UM DEVICE CADASTRADO COM ESSE MESMO SERIAL:
      
        ```json
        {
          "data": "device already registered with this serial",
          "status": "FAIL"
        }
        ```
  
## CONSULTA DE DEVICES:
- Enviar uma requisição GET para a URL: http://localhost:8989/query_device passando como parâmetro o json com o serial_number da unidade: 
    
    ```json
  {"serial_number": "123456789"}
    ```
  
- comando curl:
    ```bash
    curl --header "Content-Type: application/json" --request GET --data '{"serial_number": "123456789"}' http://localhost:8989/query_device
    ```
  
    ### RESPOSTA ESPERADA QUANDO:
  - EXISTIR UM DEVICE CADASTRADO COM O SERIAL INFORMADO:
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
    
    - NÃO EXISTIR UM DEVICE CADASTRADO COM O SERIAL INFORMADO:
    
    ```json
    {
      "data": "device was not found",
      "status": "FAIL"
    }
    ```

## INSTALANDO DEVICE CADASTRADO:
- Enviar uma requisição POST para a URL: http://localhost:8989/install_device passando como parâmetro o json com o serial_number e o endereço de instalação da unidade: 
    
    ```json
    {
    "serial_number": "123456789",
    "installation_address": "Rua D16, N55 Japiim Manaus/AM"
    }
    ```
  
- comando curl:
  
    ```bash
    curl --header "Content-Type: application/json" --request POST --data '{"serial_number": "123456789", "installation_address": "Rua D16, N55 Japiim Manaus/AM"}' http://localhost:8989/install_device
    ```
  
    ### RESPOSTA ESPERADA QUANDO:
    - O DEVICE FOR INSTALADO COM SUCESSO:
    ```json
    {
      "data": {
        "created_at": "Sun, 11 Jul 2021 13:58:20 GMT",
        "id": 1,
        "installation_address": "Rua D16, N55 Japiim Manaus/AM",
        "installation_status": 1,
        "serial_number": "123456789"
      },
      "status": "OK"
    }
    ```
    
    - NÃO EXISTIR UM DEVICE CADASTRADO COM O SERIAL INFORMADO:
    
    ```json
    {
      "data": "device was not found",
      "status": "FAIL"
    }
    ```
  
    - O DEVICE INFORMADO JÁ ESTAVA INSTALADO:
  ```json
    {
      "data": "device is already installed",
      "status": "FAIL"
    }
  ```
  
  
## DELETAR UM DEVICE:
- Enviar uma requisição DELETE para a URL: http://localhost:8989/delete_device passando como parâmetro o json com o serial_number da unidade: 
  ```json
  {"serial_number": "123456789"}
  ```
  
- comando curl:
    ```bash
    curl --header "Content-Type: application/json" --request DELETE --data '{"serial_number": "123456789"}' http://localhost:8989/delete_device
    ```
  
    ### RESPOSTA ESPERADA QUANDO:
    - O DEVICE FOR DELETADO CON SUCESSO:
    
    ```json
    {
      "data": {
        "created_at": "Sun, 11 Jul 2021 13:58:20 GMT",
        "id": 1,
        "installation_address": "Rua D16, N55 Japiim Manaus/AM",
        "installation_status": 1,
        "serial_number": "123456789"
      },
      "status": "OK"
    }
    ```
  
    - NÃO EXISTIR UM DEVICE CADASTRADO COM O SERIAL INFORMADO:
    
    ```json
    {
      "data": "device was not found",
      "status": "FAIL"
    }
    ```