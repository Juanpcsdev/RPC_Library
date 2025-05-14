import socket
from rpc.serializer import Serializer

class MathServiceStub:
    def __init__(self, binder_ip, binder_port):
        self.binder_ip = binder_ip
        self.binder_port = binder_port

    def _send_request(self, service_name, function_name, *args):
        # Conectar ao Binder para localizar o servidor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.binder_ip, self.binder_port))
            s.sendall(f"LOOKUP|{service_name}".encode())
            response = s.recv(1024).decode()

            # Verifica se a resposta do Binder está correta
            if response == "Service Not Found":
                raise ValueError(f"Serviço '{service_name}' não encontrado no Binder.")
            
            # Verifica se a resposta está no formato correto
            server_info = response.split('|')
            if len(server_info) != 2:
                raise ValueError(f"Resposta inválida do Binder. Esperado formato 'ip|port', recebido: {response}")

            server_ip = server_info[0]
            try:
                server_port = int(server_info[1])
            except ValueError:
                raise ValueError(f"Porta inválida recebida do Binder: {server_info[1]}")

        # Conectar ao servidor para chamar a função
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))
            request = {
                'function': function_name,
                'args': args
            }

            # Serializar a requisição
            serialized_request = Serializer.serialize(request)

            s.sendall(serialized_request)
            response = s.recv(1024)

            # Desserializar a resposta
            return Serializer.deserialize(response)

    def add(self, a, b):
        return self._send_request("MathService", "add", a, b)

    def subtract(self, a, b):
        return self._send_request("MathService", "subtract", a, b)

    def multiply(self, a, b):
        return self._send_request("MathService", "multiply", a, b)

    def divide(self, a, b):
        return self._send_request("MathService", "divide", a, b)