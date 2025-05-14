import unittest
from interface.math_service import MathService

class TestMathService(unittest.TestCase):
    def setUp(self):
        """Este método é chamado antes de cada método de teste ser executado."""
        self.math_service = MathService()

    def test_add(self):
        """Testa a função de adição"""
        self.assertEqual(self.math_service.add(3, 4), 7)
        self.assertEqual(self.math_service.add(-1, 1), 0)

    def test_subtract(self):
        """Testa a função de subtração"""
        self.assertEqual(self.math_service.subtract(10, 5), 5)
        self.assertEqual(self.math_service.subtract(-1, -1), 0)

    def test_multiply(self):
        """Testa a função de multiplicação"""
        self.assertEqual(self.math_service.multiply(2, 3), 6)
        self.assertEqual(self.math_service.multiply(0, 5), 0)

    def test_divide(self):
        """Testa a função de divisão"""
        self.assertEqual(self.math_service.divide(10, 2), 5)
        self.assertRaises(ValueError, self.math_service.divide, 10, 0)  # Testa a divisão por zero

if __name__ == "__main__":
    unittest.main()