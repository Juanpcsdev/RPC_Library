import socket

class Binder:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.services = {}

    def register_service(self, service_name, service_ip, service_port):
        # Verifica se o serviço já está registrado
        if service_name in self.services:
            print(f"Serviço {service_name} já registrado. Atualizando informações...")
        self.services[service_name] = (service_ip, service_port)
        print(f"Serviço '{service_name}' registrado em {service_ip}:{service_port}")

    def lookup_service(self, service_name):
        # Verifica se o serviço existe e retorna as informações
        print(f"Consultando serviço: {service_name}")
        if service_name in self.services:
            print(f"Serviço {service_name} encontrado: {self.services[service_name]}")
        else:
            print(f"Serviço {service_name} não encontrado.")
        return self.services.get(service_name, None)

    def start_binder(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as binder_socket:
            binder_socket.bind((self.host, self.port))
            binder_socket.listen(5)
            print(f"Binder iniciado em {self.host}:{self.port}...")

            while True:
                client_socket, addr = binder_socket.accept()
                with client_socket:
                    data = client_socket.recv(1024).decode()
                    print(f"Recebido do cliente: {data}")

                    if data.startswith("REGISTER"):
                        # Registro do serviço
                        _, service_name, ip, port = data.split('|')
                        self.register_service(service_name, ip, int(port))
                        client_socket.sendall(b"Service Registered")
                    elif data.startswith("LOOKUP"):
                        # Consulta de serviço
                        _, service_name = data.split('|')
                        service = self.lookup_service(service_name)
                        if service:
                            # Resposta formatada corretamente
                            response = f"{service[0]}|{service[1]}"
                        else:
                            response = "Service Not Found"
                        client_socket.sendall(response.encode())