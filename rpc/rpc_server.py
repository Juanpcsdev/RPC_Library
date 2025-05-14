import sys
import os
import socket
import threading
import time

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from interface.math_service import MathService
from rpc.serializer import Serializer

print("Iniciando a classe RPCServer...")  # Log de depuração

class RPCServer:
    def __init__(self, host='localhost', port=5001, binder_ip='localhost', binder_port=5000):
        print("Inicializando RPCServer...")
        self.host = host
        self.port = port
        self.math_service = MathService()
        self.binder_ip = binder_ip
        self.binder_port = binder_port
        self.server_socket = None

    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(4096)  # aumentei o buffer pra garantir

            if request:
                data = Serializer.deserialize(request)
                function_name = data['function']
                args = data['args']

                if hasattr(self.math_service, function_name):
                    func = getattr(self.math_service, function_name)
                    result = func(*args)
                    response = Serializer.serialize(result)
                else:
                    response = Serializer.serialize(f"Função '{function_name}' não encontrada.")

                client_socket.sendall(response)
            client_socket.close()

        except Exception as e:
            error_message = f"Erro no processamento: {str(e)}"
            response = Serializer.serialize(error_message)
            try:
                client_socket.sendall(response)
                client_socket.close()
            except:
                pass
            print(error_message)

    def register_service_to_binder(self, retries=10, delay=1):
        for attempt in range(retries):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.binder_ip, self.binder_port))
                    message = f"REGISTER|MathService|{self.host}|{self.port}"
                    s.sendall(message.encode())
                    response = s.recv(1024)
                    print(f"Resposta do Binder ao registrar serviço: {response.decode()}")
                    return  # registro bem-sucedido, sai da função
            except ConnectionRefusedError:
                print(f"Tentativa {attempt+1}/{retries}: Binder não acessível em {self.binder_ip}:{self.binder_port}. Tentando novamente em {delay}s...")
                time.sleep(delay)
        print("Não foi possível conectar ao Binder após várias tentativas. Encerrando servidor.")
        sys.exit(1)


    def start_server(self):
        print(f"Iniciando servidor RPC em {self.host}:{self.port}...")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        # Registrar serviço no Binder via socket
        self.register_service_to_binder()

        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Conexão recebida de {addr}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("Servidor encerrado manualmente.")
        finally:
            self.server_socket.close()
            print("Socket do servidor fechado.")

if __name__ == "__main__":
    server = RPCServer()
    server.start_server()