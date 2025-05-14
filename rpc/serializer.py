import pickle

class Serializer:
    @staticmethod
    def serialize(data):
        """Serializa um objeto Python em uma string de bytes."""
        return pickle.dumps(data)

    @staticmethod
    def deserialize(data):
        """Desserializa uma string de bytes de volta para o objeto Python."""
        return pickle.loads(data)