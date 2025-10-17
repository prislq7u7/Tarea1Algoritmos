from tarea1.diccionario import Diccionario

class Nodo ABB:
    def __init__(self, elemento: str):
        self.elemento = elemento#almacena el string
        self.izquierdo = None#puntero al hijo izquierdo, pero inicia como None
        self.derecho = None#puntero al hijo derecho, pero inicia como None
        