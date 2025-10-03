from .diccionario import Diccionario

class Nodo:
    def __init__(self, elemento:str=''):#constructor, se ejecuta al crear un nodo
        self.elemento = elemento #guarda la palabra
        self.siguiente: Nodo | None = None #flecha al siguiente nodo
        
    def __str__(self) -> str:
        return f"{self.elemento}"#lo imprime más bonito

class ListaOrdenadaDinámica(Diccionario):
    def __init__(self):
        self.__cabeza = Nodo()
        self.__tamaño = 0

    def __len__(self):
        return self.__tamaño
    
    def __getitem__(self, indice):
        pass

    def inserte(self, elemento):
        nuevo_nodo = Nodo(elemento)
        actual = self.__cabeza
        while actual.siguiente is not None and actual.siguiente.elemento < elemento:
            actual = actual.siguiente
        nuevo_nodo.siguiente = actual.siguiente
        actual.siguiente = nuevo_nodo
        self.__tamaño += 1

    def borre(self, elemento):
        actual = self.__cabeza
        while actual.siguiente is not None:
            if actual.siguiente.elemento == elemento:
                actual.siguiente = actual.siguiente.siguiente
                self.__tamaño -= 1
                return True
            if actual.siguiente.elemento > elemento:
                return False
            actual = actual.siguiente
        return False#llegó al final y no lo encontró

    def limpie(self):
        self.__cabeza.siguiente = None
        self.__tamaño = 0

    def miembro(self, elemento: str) -> bool:
        actual = self.__cabeza.siguiente #empieza en el primer nodo real
        
        while actual is not None:#verifica que sí haya un elemento que revisar  
            if actual.elemento == elemento:#si el elemento en el que está encima sí es el que buscaba
                return True#lo encontró
            if actual.elemento > elemento:#si el elemento en el que está encima ya es mayor al que busca
                return False#no lo va a encontrar
            actual = actual.siguiente#siguiente nodo, hasta que llegue a None
        return False#llegó al final y no lo encontró

    def imprima(self):
        print(self)

    def __str__(self) -> str:
        elementos = []
        actual = self.__cabeza.siguiente
        while actual is not None:
            elementos.append(actual.elemento)
            actual = actual.siguiente
        return " -> ".join(elementos) if elementos else "Lista vacía"
    
    def __del__(self):
        pass
    
