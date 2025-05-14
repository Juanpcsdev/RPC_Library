import sys
import os
import socket

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpc.rpc_stub_generator import MathServiceStub

def main():
    binder_ip = 'localhost'
    binder_port = 5000
    math_stub = MathServiceStub(binder_ip, binder_port)

    try:
        # Testa as operações remotas
        print("Resultado de 5 + 3:", math_stub.add(5, 3))
        print("Resultado de 4 * 2:", math_stub.multiply(4, 2))
        print("Resultado de 5 - 3:", math_stub.subtract(5, 3))
        print("Resultado de 4 / 2:", math_stub.divide(4, 2))

    except Exception as e:
        print(f"Erro crítico durante o teste: {e}")
        sys.exit(1)  # Interrompe a execução após o erro

if __name__ == "__main__":
    main()