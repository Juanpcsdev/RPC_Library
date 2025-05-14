import sys
import os

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import socket
import threading
from interface.math_service import MathService
from rpc.serializer import Serializer
from rpc.rpc_binder import Binder

class RPCServer:
    def __init__(self, host='localhost', port=5001, binder_ip='localhost', binder_port=5000):
        self.host = host
        self.port = port
        self.math_service = MathService()
        self.server_socket = None
        self.binder_ip = binder_ip
        self.binder_port = binder_port
        self.server_ready = threading.Event()  # Evento para indicar que o servidor está pronto

    def handle_client(self, client_socket):
        try:
            # Recebe a requisição do cliente
            request = client_socket.recv(1024)

            if request:
                # Desserializa a requisição
                data = Serializer.deserialize(request)
                function_name = data['function']
                args = data['args']

                # Verifica se a função existe no serviço
                if hasattr(self.math_service, function_name):
                    func = getattr(self.math_service, function_name)
                    result = func(*args)
                    response = Serializer.serialize(result)
                else:
                    response = Serializer.serialize(f"Função '{function_name}' não encontrada.")

                # Envia a resposta serializada de volta ao cliente
                client_socket.sendall(response)

        except Exception as e:
            # Em caso de erro inesperado, envia a mensagem de erro
            error_message = f"Ocorreu um erro: {str(e)}"
            response = Serializer.serialize(error_message)
            client_socket.sendall(response)

    def start_server(self):
        print("Tentando iniciar o servidor...")  # Verifique se essa linha aparece
        # Cria o socket do servidor
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor RPC iniciado em {self.host}:{self.port}...")

        # Registrar o serviço no Binder
        binder = Binder(host=self.binder_ip, port=self.binder_port)
        binder.register_service("MathService", self.host, self.port)
        print(f"Serviço MathService registrado no Binder em {self.host}:{self.port}")

        # Sinaliza que o servidor está pronto para aceitar conexões
        self.server_ready.set()

        # Aceita uma conexão (deixe o servidor funcionar por um tempo limitado)
        self.server_socket.settimeout(5)  # Tempo de espera máximo de 5 segundos
        try:
            client_socket, addr = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
        except socket.timeout:
            print("Timeout: Nenhuma conexão recebida.")
            raise RuntimeError("Erro crítico: Timeout atingido.")  # Levanta uma exceção em caso de erro
        finally:
            # Fecha o servidor após o teste
            self.server_socket.close()
            print("Servidor fechado após o teste.")