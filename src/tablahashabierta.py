from diccionario import Diccionario
from listaordenadadinamica import ListaOrdenadaDinamica

class TablaHashAbierta(Diccionario):
    
    def __init__(self, capacidad=10, carga_max=0.7):
        self.__capacidad = capacidad
        self.__carga_max = carga_max
        self.__tamanno = 0
        self.__buckets = [ListaOrdenadaDinamica() for _ in range(capacidad)]#bucket es ubicación de memoria
      
    def __len__(self):
        return self.__tamanno  