# Biblioteca RPC – Trabalho Prático Sistemas Distribuídos

Este projeto implementa uma biblioteca RPC (Remote Procedure Call) em Python usando sockets TCP, que permite que funções sejam chamadas remotamente simulando sistemas distribuídos reais. O sistema é modular, orientado a objetos e organizado para facilitar extensibilidade.

---

## Estrutura do Projeto

```bash
Library_RPC/
│
├── rpc/
│
│ ├── init.py # Inicialização do pacote RPC
│ ├── rpc_binder.py # Binder - registro e consulta de serviços
│ ├── rpc_server.py # Servidor RPC
│ ├── rpc_client.py # Cliente RPC
│ ├── rpc_stub_generator.py # Stub para chamadas remotas
│ ├── serializer.py # Serialização dos dados
│
├── interface/
│ └── math_service.py # Serviço exemplo: calculadora
│
├── examples/
│ ├── server_example.py # Exemplo de   servidor usando a biblioteca
│ └── client_example.py # Exemplo de cliente usando a biblioteca│
├── README.md # Este arquivo
```
---

## Arquitetura

A biblioteca é composta por três componentes principais:

- **Binder**: Serviço central que mantém o registro e descoberta dos servidores. Funciona como um "catálogo" de serviços registrados, respondendo a pedidos de registro e consultas.
- **Servidor RPC**: Registra seus serviços no Binder e aguarda chamadas remotas dos clientes para executar funções e retornar resultados.
- **Cliente RPC**: Consulta o Binder para descobrir a localização do serviço desejado e realiza chamadas remotas às funções disponíveis via stub.

---
## Funcionalidades


---

## Executando o Projeto

### 1. Iniciar o Binder

O Binder é o serviço que registra e disponibiliza os servidores para os clientes. Deve ser iniciado primeiro.

```bash
python rpc/rpc_binder.py
```

### 2. Iniciar o Servidor RPC

O servidor deve ser iniciado depois do Binder. Ele registra seus serviços no Binder e fica aguardando chamadas.

```bash
python rpc/rpc_server.py
```

### 3. Iniciar o Cliente RPC
O cliente consulta o Binder para descobrir o servidor que oferece o serviço e faz as chamadas remotas.

```bash
python rpc/rpc_client.py
```

---

## Como adicionar novos serviços à biblioteca



---

## Exemplos de execução

Exemplo de servidor (`example/server_example.py`)

```bash
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpc.rpc_server import RPCServer

def start_server():
    server = RPCServer(host='localhost', port=5001, binder_ip='localhost', binder_port=5000)
    print("Servidor RPC iniciado...")
    server.start_server()

if __name__ == "__main__":
    start_server()
```

---
Exemplo de cliente (`example/client_example.py`)

```bash
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpc.rpc_client import MathServiceStub

def start_client():
    binder_ip = 'localhost'
    binder_port = 5000

    math_stub = MathServiceStub(binder_ip, binder_port)
    
    print("Resultado de 5 + 3:", math_stub.add(5, 3))
    print("Resultado de 4 * 2:", math_stub.multiply(4, 2))
    print("Resultado de 5 - 3:", math_stub.subtract(5, 3))
    print("Resultado de 4 / 2:", math_stub.divide(4, 2))

if __name__ == "__main__":
    start_client()
```

---
## Considerações finais

* A biblioteca foi desenvolvida para permitir fácil extensão com novos serviços.

* Utiliza serialização com pickle para passagem transparente de objetos.

* Permite chamadas concorrentes no servidor via threads.

* Possui tratamento de erros e mecanismos de retry para tolerância a falhas.

---

## Notas Importantes



---

## Licença
Este projeto foi desenvolvido como parte de um trabalho acadêmico para a disciplina de Sistemas Distribuídos na UERJ.