import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Exemplo de cliente RPC
from rpc.rpc_client import MathServiceStub

def start_client():
    binder_ip = 'localhost'
    binder_port = 5000

    # Inicializa o stub do cliente que consulta o Binder
    math_stub = MathServiceStub(binder_ip, binder_port)
    
    # Chama as funções remotas do servidor
    print("Resultado de 5 + 3:", math_stub.add(5, 3))
    print("Resultado de 4 * 2:", math_stub.multiply(4, 2))
    print("Resultado de 5 - 3:", math_stub.subtract(5, 3))
    print("Resultado de 4 / 2:", math_stub.divide(4, 2))

if __name__ == "__main__":
    start_client()