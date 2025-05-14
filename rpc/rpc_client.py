import sys
import os
import socket
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rpc.rpc_stub_generator import MathServiceStub

def main():
    binder_ip = 'localhost'
    binder_port = 5000

    # Espera até Binder estar pronto para evitar erro de conexão
    for i in range(10):
        try:
            with socket.create_connection((binder_ip, binder_port), timeout=2) as sock:
                print("Binder acessível!")
                break
        except Exception:
            print("Aguardando Binder ficar disponível...")
            time.sleep(1)
    else:
        print("Binder não está disponível. Saindo.")
        sys.exit(1)

    math_stub = MathServiceStub(binder_ip, binder_port)

    try:
        print("Resultado de 5 + 3 =", math_stub.add(5, 3))
        print("Resultado de 4 * 2 =", math_stub.multiply(4, 2))
        print("Resultado de 5 - 3 =", math_stub.subtract(5, 3))
        print("Resultado de 4 / 2 =", math_stub.divide(4, 2))
    except Exception as e:
        print(f"Erro na chamada RPC: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()