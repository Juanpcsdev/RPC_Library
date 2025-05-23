# Biblioteca RPC – Trabalho Prático Sistemas Distribuídos

Este projeto implementa uma biblioteca RPC (Remote Procedure Call) em Python usando sockets TCP, que permite que funções sejam chamadas remotamente simulando sistemas distribuídos reais. O sistema é modular, orientado a objetos e organizado para facilitar extensibilidade.

---

## Estrutura do Projeto

```bash
Library_RPC/
│
├── rpc/
│ ├── init.py # Inicialização do pacote RPC
│ ├── rpc_binder.py # Binder - registro e consulta de serviços
│ ├── rpc_server.py # Servidor RPC
│ ├── rpc_client.py # Cliente RPC
│ ├── rpc_stub_generator.py # Stub para chamadas remotas
│ └── serializer.py # Serialização dos dados
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
### 1. Binder
* Registra serviços com nome, IP e porta para que clientes possam localizá-los.

* Responde a consultas de clientes sobre onde encontrar serviços registrados.

* Mantém o serviço ativo continuamente, aceitando múltiplas requisições.

### 2. Servidor RPC
* Registra seu serviço no Binder para que clientes possam descobri-lo.

* Executa funções remotamente para clientes, enviando resultados serializados.

* Atende múltiplas requisições simultâneas usando threads.

### 3. Cliente RPC
* Consulta o Binder para descobrir o servidor e porta do serviço desejado.

* Envia chamadas de função remotas e recebe resultados de forma transparente.

* Implementa tentativas e espera para lidar com indisponibilidade temporária do Binder ou servidor.

---

## Sobre a execução

Nesta biblioteca RPC, o Binder, o Servidor RPC e o Cliente RPC foram projetados para serem iniciados em qualquer ordem, garantindo flexibilidade no ambiente distribuído.

Cada componente possui mecanismos de tratamento que fazem com que:

* O Servidor RPC tente se conectar ao Binder repetidas vezes, aguardando até que ele esteja disponível para registrar seu serviço com sucesso.

* O Cliente RPC aguarda o Binder ficar acessível e, caso o servidor ainda não tenha registrado o serviço, realize tentativas periódicas até que o serviço seja encontrado.

* O Binder fica sempre ativo, aguardando conexões de registro e consultas, não dependendo da ordem de inicialização dos demais.

## Como executar
Cada componente (Binder, Servidor e Cliente) deve ser executado em um console/terminal separado para que fiquem rodando simultaneamente e possam se comunicar entre si.

### 1. Iniciar o Binder em um terminal

O Binder é o serviço que registra e disponibiliza os servidores para os clientes.

```bash
python rpc/rpc_binder.py
```

### 2. Iniciar o Servidor RPC em outro terminal

Ele registra seus serviços no Binder e fica aguardando chamadas.

```bash
python rpc/rpc_server.py
```

### 3. Iniciar o Cliente RPC em um terceiro terminal
O Cliente consulta o Binder para descobrir o servidor que oferece o serviço e faz as chamadas remotas.

```bash
python rpc/rpc_client.py
```

---

## Como adicionar novos serviços à biblioteca
Vamos simular a criação de um serviço que realiza conversão direta entre Fahrenheit e Celsius. Este exemplo mostrará passo a passo como integrar um novo serviço à biblioteca RPC, desde a implementação da lógica até a exposição via servidor e o consumo pelo cliente.

### 1. Criando o arquivo de serviço
Na pasta `/interface` crie o arquivo `temperature_servive.py` e adicione a implementação da lógica de conversão:

```bash 
class TemperatureService:
    def celsius_to_fahrenheit(self, c):
        return c * 9/5 + 32

    def fahrenheit_to_celsius(self, f):
        return (f - 32) * 5/9
```
### 2. Adaptando o servidor RPC para expor o novo serviço
No código atual `rpc_server.py`, substitua a instância do serviço atual pela do novo serviço `TemperatureService`.

Altere o método que encaminha as chamadas para o serviço:

Linha 10:
```bash
from interface.temperature_service import TemperatureService
```

Linha 20:
```bash
self.service_name = TemperatureService()
```

Linhas 60 (**OPCIONAL**, Apenas para deixar melhor visualmente):
```bash
message = f"REGISTER|TemperatureService|{self.host}|{self.port}"
```

### 3. Adaptando o Stub generator para o novo serviço
No código atual `rpc_stub_generator.py`, crie uma nova classe de stub para o `TemperatureService`. 

Altere com os métodos correspondentes:

Linha 5:
```bash
class TemperatureServiceStub:
```

Linha 53 até a 63:
```bash
def celsius_to_fahrenheit(self, c):
        return self._send_request("TemperatureService", "celsius_to_fahrenheit", c)

    def fahrenheit_to_celsius(self, f):
        return self._send_request("TemperatureService", "fahrenheit_to_celsius", f)
```

### 4. Adaptando o Init para o novo serviço
No código atual `__init__.py`, importe o novo stub para que ele fique disponível para os clientes. 

Altere com os métodos correspondentes:

Linha 3:
```bash
from .rpc_client import TemperatureServiceStub
```

### 5. Adaptando o Client para o novo serviço
No código atual `rpc_client.py`, importe o novo stub e crie um cliente para testar o serviço.

Altere com os métodos correspondentes:

Linha 9:
```bash
from rpc.rpc_stub_generator import TemperatureServiceStub
```

Linha 28:
```bash
temp_stub = TemperatureServiceStub(binder_ip, binder_port)
```

Linha 32 até a 35:
```bash
print("100 Celsius em Fahrenheit:", temp_stub.celsius_to_fahrenheit(100))
print("212 Fahrenheit em Celsius:", temp_stub.fahrenheit_to_celsius(212))
```
Agora, basta seguir a sessão **Como executar** para iniciar o Binder, servidor e cliente normalmente.

---

## Exemplos de execução

⚠️ Modelo baseado no serviço `math_service.py`⚠️

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


---

## Notas Importantes ⚠️

* **Limitações:** Este sistema é uma simulação didática de RPC e não possui mecanismos avançados de segurança, autenticação ou criptografia. Não é recomendado para uso em ambientes produtivos sem adaptações.

* **Extensibilidade:** A arquitetura modular permite adicionar novos serviços facilmente, desde que respeitem a interface de serialização e registro no Binder.

* **Tratamento de erros:** O sistema inclui tratamento básico para serviços não encontrados, funções inexistentes e indisponibilidade temporária dos componentes.

---

## Licença
Este projeto foi desenvolvido como parte de um trabalho acadêmico para a disciplina de Sistemas Distribuídos na UERJ.