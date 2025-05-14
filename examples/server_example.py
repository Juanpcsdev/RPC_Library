# Exemplo de servidor RPC
from rpc.rpc_binder import Binder
from rpc.rpc_server import RPCServer

def start_server():
    # Inicializa o Binder na porta 5000
    binder = Binder(host='localhost', port=5000)
    binder.start_binder()  # Inicia o Binder

    # Inicializa o servidor RPC na porta 5001
    server = RPCServer(host='localhost', port=5001)
    print("Servidor RPC iniciado...")
    
    # Registrar o serviço MathService no Binder
    binder.register_service("MathService", 'localhost', 5001)
    
    # Iniciar o servidor para escutar as requisições
    server.start_server()

if __name__ == "__main__":
    start_server()
