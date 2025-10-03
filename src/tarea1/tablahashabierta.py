from .diccionario import Diccionario


#fom listaordenadadinamica import ListaOrdenadaDinamica#cada bucket es una lista ordenada dinámica

class TablaHashAbierta(Diccionario):#herencia de Diccionario
    pass
    
""""
    def __init__(self, capacidad=10, carga_max=0.7):
        self.__capacidad = capacidad
        self.__carga_max = carga_max
        self.__tamanno = 0
        self.__buckets = [ListaOrdenadaDinamica() for F in range(capacidad)]#bucket es ubicación de memoria
      
    def __len__(self):
        return self.__tamanno  
    
    def __funcion_hash(self, elemento: str) -> int:#función para strings
        val_hash = 0
        for char in elemento:
            val_hash = (val_hash * 31 + ord(char)) % self.__capacidad
        return val_hash
"""