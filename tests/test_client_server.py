import unittest
import socket
import threading
from rpc.rpc_binder import Binder
from rpc.rpc_server import RPCServer
from rpc.rpc_client import MathServiceStub
import time

class TestClientServerCommunication(unittest.TestCase):
    def setUp(self):
        """Configura o ambiente de teste: iniciar o Binder e o Servidor"""
        # Evento para sincronizar quando o servidor estiver pronto
        self.server_ready_event = threading.Event()

        # Inicia o Binder na porta 5000
        self.binder_thread = threading.Thread(target=self.start_binder)
        self.binder_thread.start()

        # Inicia o servidor RPC na porta 5001
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.start()

        # Espera até que o servidor esteja pronto para aceitar conexões
        self.server_ready_event.wait()  # Espera até o evento ser sinalizado

    def start_binder(self):
        """Função para iniciar o Binder (chamada diretamente como o professor pediu)"""
        binder = Binder(host='localhost', port=5000)
        binder.start_binder()  # Chama a função `start_binder()` como no PDF

    def start_server(self):
        """Função para iniciar o servidor"""
        server = RPCServer(host='localhost', port=5001)

        # Registra o serviço MathService no Binder
        binder = Binder(host='localhost', port=5000)
        binder.register_service("MathService", 'localhost', 5001)
        print("Serviço MathService registrado no Binder.")

        # Indica que o servidor está pronto para aceitar conexões
        self.server_ready_event.set()

        server.start_server()  # Inicia o servidor RPC

    def test_client_server_communication(self):
        """Testa a comunicação entre o cliente e o servidor"""
        try:
            # Configura o cliente
            client = MathServiceStub(binder_ip='localhost', binder_port=5000)

            # Testa as operações remotas
            result = client.add(5, 3)
            self.assertEqual(result, 8)

        except Exception as e:
            # Se houver qualquer erro, imprime a mensagem e interrompe o teste
            print(f"Erro crítico durante o teste: {e}")
            self.fail(f"Teste falhou devido a: {str(e)}")

    def tearDown(self):
        """Finaliza o ambiente de teste: para o servidor e o Binder"""
        # Finaliza os threads (você pode implementar uma lógica para parar o Binder e o Servidor)
        self.binder_thread.join()
        self.server_thread.join()

if __name__ == "__main__":
    unittest.main()