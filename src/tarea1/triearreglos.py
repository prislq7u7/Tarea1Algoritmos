from tarea1.diccionario import Diccionario

class TrieArreglos(Diccionario):
    
    # Implementa un diccionario usando un Trie con arreglos fijos. 
    # Cada nodo tiene 26 posibles caminos, uno por cada letra del abecedario.
    
    def __init__(self):
        # nodo raíz vacío
        self.__raiz = NodoTrieArr()  
        # Número de palabras guardadas
        self.__tamanno = 0  

    def inserte(self, palabra: str):
        # Inserta una palabra en el Trie.
        # Crea nodos nuevos cuando no existen.
        actual = self.__raiz
        for letra in palabra:
            i = indice_letra(letra)
            # Si no hay nodo hijo para esta letra, se crea uno
            if actual.hijos[i] is None:
                actual.hijos[i] = NodoTrieArr()
            # Avanza al siguiente nodo
            actual = actual.hijos[i]
        # Marca el final de la palabra (si antes no existía)
        if not actual.fin_palabra:
            actual.fin_palabra = True
            self.__tamanno += 1

    def miembro(self, palabra: str) -> bool:
        # Verifica si una palabra está en el Trie.
        actual = self.__raiz
        for letra in palabra:
            i = indice_letra(letra)
            # Si en algún punto falta el nodo, la palabra no existe
            if actual.hijos[i] is None:
                return False
            actual = actual.hijos[i]
        # Solo retorna True si el nodo final marca fin de palabra
        return actual.fin_palabra

    def borre(self, palabra: str) -> bool:
        # Elimina una palabra del Trie.
        # Limpia nodos vacíos de forma recursiva.
        def eliminar(nodo, palabra, indice):
            # Si el nodo es None, no hay nada que borrar
            if nodo is None:
                return False

            # Caso base: final de palabra
            if indice == len(palabra):
                if not nodo.fin_palabra:
                    return False
                nodo.fin_palabra = False
                self.__tamanno -= 1
                # Retorna True si el nodo no tiene hijos
                return all(hijo is None for hijo in nodo.hijos)

            # Avanza al siguiente nodo según la letra actual
            i = indice_letra(palabra[indice])
            puede_eliminar = eliminar(nodo.hijos[i], palabra, indice + 1)

            # Si el hijo puede eliminarse, se elimina del arreglo
            if puede_eliminar:
                nodo.hijos[i] = None
                # Retorna True si este nodo también puede eliminarse
                return not nodo.fin_palabra and all(h is None for h in nodo.hijos)
            return False

        # Empieza el borrado desde la raíz
        return eliminar(self.__raiz, palabra, 0)

    def limpie(self):
        # Limpia completamente el Trie.
        self.__raiz = NodoTrieArr()
        self.__tamanno = 0

    def __inorden(self, nodo, prefijo, resultado):
        # Recorre el Trie de manera ordenada (a..z), construyendo las palabras completas.
        if nodo is None:
            return

        if nodo.fin_palabra:
            resultado.append(prefijo)

        for i in range(26):
            if nodo.hijos[i] is not None:
                # convierte índice a letra
                letra = chr(i + ord('a'))  
                self.__inorden(nodo.hijos[i], prefijo + letra, resultado)

    def imprima(self):
        #Imprime el contenido del Trie.
        print(self)

    def __str__(self):
        #Retorna una representación textual de todas las palabras almacenadas.
        palabras = []
        self.__inorden(self.__raiz, "", palabras)
        return ", ".join(palabras) if palabras else "Trie vacío"

    def __len__(self):
        # Retorna el número de palabras almacenadas.
        return self.__tamanno
    
    # Función auxiliar para convertir una letra (a..z) en índice (0..25)
def indice_letra(letra: str) -> int:
    return ord(letra) - ord('a')


class NodoTrieArr:
    def __init__(self):
        # Cada nodo tiene un arreglo de 26 posiciones (una por cada letra)
        self.hijos = [None] * 26
        # indica si termina una palabra
        self.fin_palabra = False