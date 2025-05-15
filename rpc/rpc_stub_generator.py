import socket
import time
from rpc.serializer import Serializer

class MathServiceStub:
    def __init__(self, binder_ip, binder_port):
        self.binder_ip = binder_ip
        self.binder_port = binder_port

    def _send_request(self, service_name, function_name, *args, retries=10, delay=1):
        for attempt in range(retries):
            try:
                # Conecta ao Binder para localizar o servidor
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.binder_ip, self.binder_port))
                    s.sendall(f"LOOKUP|{service_name}".encode())
                    response = s.recv(1024).decode()

                if response == "Service Not Found":
                    # Serviço ainda não registrado, aguarda e tenta novamente
                    print(f"Tentativa {attempt+1}/{retries}: Serviço '{service_name}' não encontrado no Binder. Aguardando servidor registrar...")
                    time.sleep(delay)
                    continue  # Tenta novamente

                server_ip, server_port = response.split('|')
                server_port = int(server_port)

                # Conecta ao servidor para enviar a requisição
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

            except ConnectionRefusedError:
                # Binder ou servidor indisponível, tenta novamente após delay
                print(f"Tentativa {attempt+1}/{retries}: Não foi possível conectar ao Binder ou Servidor. Tentando novamente em {delay}s...")
                time.sleep(delay)
            except Exception as e:
                # Outros erros inesperados também resultam em retry
                print(f"Erro inesperado: {e}")
                time.sleep(delay)

        # Após tentativas, falha definitiva
        raise RuntimeError(f"Falha na comunicação RPC: serviço '{service_name}' não disponível após {retries} tentativas.")

    # Métodos remotos disponíveis para o cliente
    def add(self, a, b):
        return self._send_request("MathService", "add", a, b)

    def subtract(self, a, b):
        return self._send_request("MathService", "subtract", a, b)

    def multiply(self, a, b):
        return self._send_request("MathService", "multiply", a, b)

    def divide(self, a, b):
        return self._send_request("MathService", "divide", a, b)