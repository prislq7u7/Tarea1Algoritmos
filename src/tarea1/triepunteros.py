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
            # Si no existe un nodo hijo para esta letra, se crea un nuevo nodo
            if letra not in actual.hijos:
                actual.hijos[letra] = NodoTriePunteros()
            # Avanza al siguiente nodo hijo correspondiente a la letra actual
            actual = actual.hijos[letra]
            
        # Al finalizar la palabra, marca este nodo como fin de palabra
        if not actual.fin_palabra:
            actual.fin_palabra = True
            # Aumenta el contador solo si es palabra nueva
            self.__tamanno += 1  

    def miembro(self, palabra: str) -> bool:
        # Verifica si una palabra está almacenada en el trie.
        actual = self.__raiz
        # Recorre cada letra de la palabra
        for letra in palabra:
            # Si falta alguna letra, la palabra no existe
            if letra not in actual.hijos:
                return False
            actual = actual.hijos[letra]
        # La palabra existe solo si el último nodo marca fin de palabra
        return actual.fin_palabra

    def borre(self, palabra: str) -> bool:
        # Elimina una palabra del trie y devuelve True si fue eliminada.
        def eliminar(nodo, palabra, indice):
            # Caso base: llega al final de la palabra
            if indice == len(palabra):
                # Si este nodo no marcaba fin de palabra, no había palabra que borrar
                if not nodo.fin_palabra:
                    return False
                
                # Marca que ya no es fin de palabra
                nodo.fin_palabra = False
                # Este nodo puede eliminarse si no tiene hijos
                return len(nodo.hijos) == 0

            letra = palabra[indice]
            # Si la letra actual no está en los hijos, la palabra no existe
            if letra not in nodo.hijos:
                return False

            # Llamada recursiva para seguir bajando por la palabra
            puede_eliminar = eliminar(nodo.hijos[letra], palabra, indice + 1)

            # Si el hijo puede eliminarse, se borra del diccionario de hijos
            if puede_eliminar:
                del nodo.hijos[letra]
                # Este nodo puede eliminarse si no es fin de palabra y no tiene hijos
                return not nodo.fin_palabra and len(nodo.hijos) == 0
            return False

        # Verifica si la palabra está en el trie
        if self.miembro(palabra):
            # Llama a la función recursiva de eliminación
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
        # Si este nodo marca fin de palabra, agrega la palabra completa (prefijo)
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
        # Inicialmente vacío, se llena según las palabras insertadas
        self.hijos = {}
        # Indica si este nodo marca el final de una palabra válida
        self.fin_palabra = False