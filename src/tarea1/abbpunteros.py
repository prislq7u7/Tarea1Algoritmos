from tarea1.diccionario import Diccionario

class NodoABB:
    def __init__(self, elemento: str):
        self.elemento = elemento#almacena el string
        self.izquierdo = None#puntero al hijo izquierdo, pero inicia como None
        self.derecho = None#puntero al hijo derecho, pero inicia como None
        
class ABBPunteros(Diccionario):
    def __init__(self):
        self.__raiz: NodoABB | None = None#puntero a la raiz, inicia como None
        self.__tamanno = 0#contador de elementos en el árbol
        