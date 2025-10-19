from tarea1.diccionario import Diccionario

class TriePunteros(Diccionario):
    def __init__(self):
        # Crea el nodo raíz del trie
        self.__raiz = NodoTriePunteros()  
        # Contador de palabras en el trie
        self.__tamanno = 0  
        
    def inserte(self, palabra: str):
        actual = self.__raiz
        for letra in palabra:
            # si la letra no existe aún, se crea el nodo hijo
            if letra not in actual.hijos:
                actual.hijos[letra] = NodoTriePunteros()
            # Baja al siguiente nodo
            actual = actual.hijos[letra]  
        if not actual.fin_palabra:
            actual.fin_palabra = True
            # Cuenta nuevas palabras
            self.__tamanno += 1  

    def miembro(self, palabra: str) -> bool:
        actual = self.__raiz
        for letra in palabra:
            # Si alguna letra no está, la palabra no existe
            if letra not in actual.hijos:
                return False
            actual = actual.hijos[letra]
        # true solo si era palabra completa
        return actual.fin_palabra  

    def borre(self, palabra: str) -> bool:
        # se apoya en una función recursiva
        def eliminar(nodo, palabra, indice):
            if indice == len(palabra):
                if not nodo.fin_palabra:
                    return False  # no existe la palabra
                nodo.fin_palabra = False
                self.__tamanno -= 1
                # retorna True si el nodo puede eliminarse
                return len(nodo.hijos) == 0
            letra = palabra[indice]
            if letra not in nodo.hijos:
                return False  # la palabra no existe
            puede_eliminar = eliminar(nodo.hijos[letra], palabra, indice + 1)
            if puede_eliminar:
                del nodo.hijos[letra]
                # se puede eliminar si ya no tiene hijos ni es fin de palabra
                return not nodo.fin_palabra and len(nodo.hijos) == 0
            return False

        return eliminar(self.__raiz, palabra, 0)

    def limpie(self):
        # limpia todo el trie
        self.__raiz = NodoTriePunteros()
        self.__tamanno = 0

    def __inorden(self, nodo, prefijo, resultado):
        # recorre el trie para obtener las palabras ordenadas alfabéticamente
        if nodo.fin_palabra:
            resultado.append(prefijo)
        for letra in sorted(nodo.hijos.keys()):
            self.__inorden(nodo.hijos[letra], prefijo + letra, resultado)

    def imprima(self):
        print(self)

    def __str__(self) -> str:
        palabras = []
        self.__inorden(self.__raiz, "", palabras)
        return ", ".join(palabras) if palabras else "Trie vacío"

    def __len__(self):
        return self.__tamanno
    
class NodoTriePunteros:
    def __init__(self):
        # Cada nodo tiene punteros a sus hijos (uno por cada letra de la 'a' a la 'z')
        # se usa un diccionario para mapear letra → nodo hijo
        self.hijos = {}
        # Marca si una palabra termina en este nodo
        self.fin_palabra = False 