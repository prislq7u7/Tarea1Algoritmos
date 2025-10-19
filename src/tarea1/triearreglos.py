from tarea1.diccionario import Diccionario

class TrieArreglos(Diccionario):
    def __init__(self):
        # Nodo raíz del trie (vacío)
        self.__raiz = NodoTrieArr()
        # Contador de palabras almacenadas
        self.__tamanno = 0  

    def inserte(self, palabra: str):
        # Inserta una palabra en el trie, creando nodos nuevos si es necesario.
        actual = self.__raiz
        for letra in palabra:
            i = self.__indice_letra(letra)
            # Si no hay nodo hijo en esa posición, se crea
            if actual.hijos[i] is None:
                actual.hijos[i] = NodoTrieArr()
            actual = actual.hijos[i]
        # Marca el fin de la palabra
        if not actual.fin_palabra:
            actual.fin_palabra = True
            self.__tamanno += 1

    def miembro(self, palabra: str) -> bool:
        # Verifica si una palabra está almacenada en el trie.
        actual = self.__raiz
        for letra in palabra:
            i = self.__indice_letra(letra)
            if actual.hijos[i] is None:
                return False
            actual = actual.hijos[i]
        return actual.fin_palabra

    def borre(self, palabra: str) -> bool:
        # Elimina una palabra del trie y devuelve True si fue eliminada.
        def eliminar(nodo, palabra, indice):
            # Si el nodo no existe, no hay nada que borrar
            if nodo is None:
                return False

            # Caso base: llegamos al final de la palabra
            if indice == len(palabra):
                if not nodo.fin_palabra:
                    return False  # No era palabra guardada
                nodo.fin_palabra = False
                # Retorna True si el nodo puede eliminarse (sin hijos)
                return all(hijo is None for hijo in nodo.hijos)

            # Avanza a la siguiente letra
            i = self.__indice_letra(palabra[indice])
            puede_eliminar = eliminar(nodo.hijos[i], palabra, indice + 1)

            # Si el hijo puede eliminarse, se limpia su referencia
            if puede_eliminar:
                nodo.hijos[i] = None
                # Retorna True si este nodo también puede eliminarse
                return not nodo.fin_palabra and all(h is None for h in nodo.hijos)
            return False

        # Si la palabra existe, la eliminamos
        if self.miembro(palabra):
            eliminar(self.__raiz, palabra, 0)
            self.__tamanno -= 1  # Siempre que la palabra existía, reduce el contador
            return True
        else:
            return False

    def limpie(self):
        # Reinicia completamente el trie.
        self.__raiz = NodoTrieArr()
        self.__tamanno = 0

    def __inorden(self, nodo, prefijo, resultado):
        # Recorrido ordenado (de 'a' a 'z') para reconstruir las palabras.
        if nodo is None:
            return
        if nodo.fin_palabra:
            resultado.append(prefijo)
        for i in range(26):
            if nodo.hijos[i] is not None:
                letra = chr(i + ord('a'))
                self.__inorden(nodo.hijos[i], prefijo + letra, resultado)

    def imprima(self):
        # Imprime todas las palabras almacenadas.
        print(self)

    def __str__(self) -> str:
        # Devuelve un string con todas las palabras del trie.
        palabras = []
        self.__inorden(self.__raiz, "", palabras)
        return ", ".join(palabras) if palabras else "Trie vacío"

    def __len__(self):
        # Devuelve el número total de palabras guardadas.
        return self.__tamanno

    def __indice_letra(self, letra: str) -> int:
        # Convierte una letra minúscula (a-z) a índice (0-25).
        return ord(letra) - ord('a')


class NodoTrieArr:
    def __init__(self):
        # Cada nodo tiene 26 posibles hijos, uno por cada letra del alfabeto
        self.hijos = [None] * 26
        # Indica si el nodo representa el fin de una palabra
        self.fin_palabra = False