import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpc.rpc_server import RPCServer

def start_server():
    server = RPCServer(host='localhost', port=5001, binder_ip='localhost', binder_port=5000)
    print("Servidor RPC iniciado...")
    server.start_server()

if __name__ == "__main__":
    start_server()
