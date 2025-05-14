import socket
from rpc.serializer import Serializer

class MathServiceStub:
    def __init__(self, binder_ip, binder_port):
        self.binder_ip = binder_ip
        self.binder_port = binder_port

    def _send_request(self, service_name, function_name, *args):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.binder_ip, self.binder_port))
                s.sendall(f"LOOKUP|{service_name}".encode())
                response = s.recv(1024).decode()

            if response == "Service Not Found":
                raise ValueError(f"Serviço '{service_name}' não encontrado no Binder.")
            
            server_ip, server_port = response.split('|')
            server_port = int(server_port)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((server_ip, server_port))
                request = {
                    'function': function_name,
                    'args': args
                }
                serialized_request = Serializer.serialize(request)
                s.sendall(serialized_request)
                response = s.recv(4096)
                return Serializer.deserialize(response)

        except Exception as e:
            raise RuntimeError(f"Erro na comunicação RPC: {e}")

    def add(self, a, b):
        return self._send_request("MathService", "add", a, b)

    def subtract(self, a, b):
        return self._send_request("MathService", "subtract", a, b)

    def multiply(self, a, b):
        return self._send_request("MathService", "multiply", a, b)

    def divide(self, a, b):
        return self._send_request("MathService", "divide", a, b)