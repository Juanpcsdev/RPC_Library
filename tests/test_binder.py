import unittest
from rpc.rpc_binder import Binder

class TestBinder(unittest.TestCase):
    def setUp(self):
        """Configura o ambiente de teste antes de cada teste"""
        self.binder = Binder(host='localhost', port=5000)

    def test_register_service(self):
        """Testa o registro de serviço"""
        self.binder.register_service("MathService", "localhost", 5001)
        service = self.binder.lookup_service("MathService")
        self.assertIsNotNone(service)  # O serviço deve ser encontrado
        self.assertEqual(service, ("localhost", 5001))  # Verifica se o serviço foi registrado corretamente

    def test_lookup_service(self):
        """Testa a consulta de serviço"""
        self.binder.register_service("MathService", "localhost", 5001)
        service = self.binder.lookup_service("MathService")
        self.assertEqual(service, ("localhost", 5001))

    def test_service_not_found(self):
        """Testa o caso de serviço não encontrado"""
        service = self.binder.lookup_service("NonExistentService")
        self.assertIsNone(service)  # Espera-se que nenhum serviço seja encontrado

if __name__ == "__main__":
    unittest.main()