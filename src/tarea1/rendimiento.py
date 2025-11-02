from tarea1.diccionario import Diccionario
from tarea1.listaordenadadinamica import ListaOrdenadaDinámica
from tarea1.listaordenadaestatica import ListaOrdenadaEstática
from tarea1.tablahashabierta import TablaHashAbierta
from tarea1.abbpunteros import ABBPunteros
from tarea1.abbvectorheap import ABBVectorHeap
from tarea1.triepunteros import TriePunteros
from tarea1.triearreglos import TrieArreglos

#En este archivo crearemos las pruebas de rendimiento

class Rendimiento():
    
    def __init__(self):
        self.tamanos = [100, 50000, 1000000]
        self.repeticiones = 10
        self.estructuras = {
            "ListaOrdenadaDinámica": ListaOrdenadaDinámica,
            "ListaOrdenadaEstática": lambda: ListaOrdenadaEstática(1000000),
            "TablaHashAbierta": TablaHashAbierta,
            "ABBPunteros": ABBPunteros,
            "ABBVectorHeap": ABBVectorHeap,
            "TriePunteros": TriePunteros,
            "TrieArreglos": TrieArreglos
        }
    
    def generador_palaras(self):
        pass