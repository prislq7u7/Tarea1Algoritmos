from tarea1.diccionario import Diccionario

class TriePunteros(Diccionario):
    def __init__(self):
        # Se crea el nodo raíz del trie (vacío al inicio)
        self.__raiz = NodoTriePunteros()
        # Contador de palabras almacenadas
        self.__tamanno = 0  

    def inserte(self, palabra: str):
        # Inserta una palabra letra por letra en el trie.
        actual = self.__raiz
        for letra in palabra:
            # Si la letra no existe en los hijos, se crea un nuevo nodo
            if letra not in actual.hijos:
                actual.hijos[letra] = NodoTriePunteros()
            # Avanza al siguiente nodo
            actual = actual.hijos[letra]
        # Marca el final de una palabra completa
        if not actual.fin_palabra:
            actual.fin_palabra = True
            # Aumenta el contador solo si es palabra nueva
            self.__tamanno += 1  

    def miembro(self, palabra: str) -> bool:
        # Verifica si una palabra está almacenada en el trie.
        actual = self.__raiz
        for letra in palabra:
            # Si falta alguna letra, la palabra no existe
            if letra not in actual.hijos:
                return False
            actual = actual.hijos[letra]
        return actual.fin_palabra  # True solo si marca fin de palabra

    def borre(self, palabra: str) -> bool:
        # Elimina una palabra del trie y devuelve True si fue eliminada.
        def eliminar(nodo, palabra, indice):
            # Caso base: llegamos al final de la palabra
            if indice == len(palabra):
                if not nodo.fin_palabra:
                    return False  # La palabra no estaba guardada
                nodo.fin_palabra = False
                # True si este nodo ya no tiene hijos (se puede borrar)
                return len(nodo.hijos) == 0

            letra = palabra[indice]
            if letra not in nodo.hijos:
                return False  # La palabra no existe

            # Llamada recursiva para seguir bajando por la palabra
            puede_eliminar = eliminar(nodo.hijos[letra], palabra, indice + 1)

            # Si el hijo puede eliminarse, lo borramos del diccionario de hijos
            if puede_eliminar:
                del nodo.hijos[letra]
                # Retorna True si este nodo también puede eliminarse
                return not nodo.fin_palabra and len(nodo.hijos) == 0
            return False

        # Primero verificamos si la palabra está en el trie
        if self.miembro(palabra):
            eliminar(self.__raiz, palabra, 0)
            # Reduce el contador si existe
            self.__tamanno -= 1  
            return True
        else:
            return False

    def limpie(self):
        # Limpia completamente el trie, eliminando todas las palabras.
        self.__raiz = NodoTriePunteros()
        self.__tamanno = 0

    def __inorden(self, nodo, prefijo, resultado):
        # Recorrido inorden alfabético, generando las palabras completas.
        if nodo.fin_palabra:
            resultado.append(prefijo)
        # Ordena las letras para mantener salida alfabética
        for letra in sorted(nodo.hijos.keys()):
            self.__inorden(nodo.hijos[letra], prefijo + letra, resultado)

    def imprima(self):
        #Imprime todas las palabras almacenadas.
        print(self)

    def __str__(self) -> str:
        # Devuelve un string con todas las palabras del trie.
        palabras = []
        self.__inorden(self.__raiz, "", palabras)
        return ", ".join(palabras) if palabras else "Trie vacío"

    def __len__(self):
        # Devuelve el número total de palabras guardadas.
        return self.__tamanno


class NodoTriePunteros:
    def __init__(self):
        # Cada nodo guarda sus hijos en un diccionario (letra → nodo hijo)
        self.hijos = {}
        # Indica si este nodo marca el final de una palabra válida
        self.fin_palabra = False