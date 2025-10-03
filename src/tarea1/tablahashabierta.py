from .diccionario import Diccionario
from .listaordenadadinamica import ListaOrdenadaDinamica#cada bucket es una lista ordenada dinámica

class TablaHashAbierta(Diccionario):#herencia de Diccionario
    
    def __init__(self, capacidad=10, carga_max=0.7):#constructor
        self.__capacidad = capacidad #número de buckets de la tabla hash
        self.__carga_max = carga_max #factor de carga máximo permitido
        self.__tamanno = 0 #cuántps elementos hay en total
        self.__buckets = [ListaOrdenadaDinamica() for F in range(capacidad)]#bucket es ubicación de memoria, crea array de listas vacías, c/u lista es un bucket
      
    def __len__(self):
        return self.__tamanno  
    
    def __funcion_hash(self, elemento: str) -> int:#función para convertir string a número para saber en qué bucket va
        val_hash = 0
        for char in elemento:
            val_hash = (val_hash * 31 + ord(char)) % self.__capacidad#ord(char) da valor ASCII
        return val_hash
    
    def inserte(self, elemento : str):
        if self.__factor_carga() >= self.__carga_max:
            self.__redimensionar(self.__capacidad * 2)#si la tabla está muy llena se duplica su tamaño
    
    