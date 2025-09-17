from abc import ABC, abstractmethod

class Diccionario(ABC):
    @abstractmethod
    def inserte(self, elemento):
        """
        Inserta un elmento. Puede ser repetido.
        """
        pass

    @abstractmethod
    def borre(self, elemento):
        pass

    @abstractmethod
    def limpie(self):
        pass

    @abstractmethod
    def miembro(self, elemento):
        pass

    @abstractmethod
    def imprima(self):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
