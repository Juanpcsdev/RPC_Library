import socket

class Binder:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.services = {} # Dicionário para armazenar serviços registrados

    def register_service(self, service_name, service_ip, service_port):
        if service_name in self.services:
            print(f"Atualizando serviço {service_name} para {service_ip}:{service_port}")
        else:
            print(f"Registrando serviço {service_name} em {service_ip}:{service_port}")
        self.services[service_name] = (service_ip, service_port)

    def lookup_service(self, service_name):
        print(f"Buscando serviço: {service_name}")
        return self.services.get(service_name, None)

    def start_binder(self):
        print(f"Binder iniciado em {self.host}:{self.port}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port)) # Liga o socket à porta
                s.listen(5) # Escuta conexões (máximo 5 na fila)

                while True:
                    client_socket, addr = s.accept() # Aceita nova conexão
                    with client_socket:
                        try:
                            data = client_socket.recv(1024).decode() # Recebe dados do cliente
                            print(f"Recebido do cliente: {data}")

                            if data.startswith("REGISTER"):
                                # Registro de novo serviço
                                _, service_name, ip, port = data.split('|')
                                self.register_service(service_name, ip, int(port))
                                client_socket.sendall(b"Service Registered")

                            elif data.startswith("LOOKUP"):
                                # Consulta de serviço
                                _, service_name = data.split('|')
                                service = self.lookup_service(service_name)
                                if service:
                                    response = f"{service[0]}|{service[1]}"
                                else:
                                    response = "Service Not Found"
                                client_socket.sendall(response.encode())
                        except Exception as e:
                            print(f"Erro ao processar cliente {addr}: {e}")
        except KeyboardInterrupt:
            print("\nBinder encerrado pelo usuário.")
        except Exception as e:
            print(f"Erro crítico no Binder: {e}")

if __name__ == "__main__":
    binder = Binder()
    binder.start_binder()
