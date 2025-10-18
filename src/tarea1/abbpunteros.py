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
        
    def findNodo(self, elemento:str, nodo: NodoABB | None) -> NodoABB | None:
        if nodo is None or nodo.elemento == elemento:#si llega al final o encuentra el elemento
            return nodo#retorna el nodo encontrado o None
        if elemento < nodo.elemento:#si el elemento buscado es menor
            return self.findNodo(elemento, nodo.izquierdo)#busca en el subárbol izquierdo
        return self.findNodo(elemento, nodo.derecho)#si es mayor, busca en el subárbol derecho
        
    def insertarNodo(self, elemento:str, nodo: NodoABB | None) -> NodoABB:
        if nodo is None:#si llega a una posición vacía
            self.__tamanno += 1#incrementa el contador de elementos
            return NodoABB(elemento)#crea y retorna nuevo nodo
        
        if elemento < nodo.elemento:#si el elemento es menor
            nodo.izquierdo = self.insertarNodo(elemento, nodo.izquierdo)#inserta en el izquierdo
        elif elemento > nodo.elemento:#si el elemento es mayor
            nodo.derecho = self.insertarNodo(elemento, nodo.derecho)#inserta en el derecho
        return nodo#retorna el nodo actual(puede ser modificado o no)
    
    def findMinimo(self, nodo: NodoABB) -> NodoABB:
        actual = nodo#comeinza desde el nodo que se le pasa
        while actual.izquierdo is not None:#mientras haya un hijo izquierdo
            actual = actual.izquierdo#baja por la izquierda
        return actual#retorna el nodo más a la izquierda
    
    def eliminarNodo(self, elemento:str, nodo: NodoABB | None) -> NodoABB | None:   
        if nodo is None:#si el arbol esta vacio o elemento notFound
            return None
        
        if elemento < nodo.elemento:#si el elemento es menor
            nodo.izquierdo = self.eliminarNodo(elemento, nodo.izquierdo)#busca en el izquierdo
        elif elemento > nodo.elemento:#si el elemento es mayor
            nodo.derecho = self.eliminarNodo(elemento, nodo.derecho)#busca en el derecho
        else:#si encuentra el elemento
            
            #primer caso: nodo sin hijo izquierdo
            if nodo.izquierdo is None:
                self.__tamanno -= 1#decrementa el contador
                return nodo.derecho#reemplaza ntonces por el hijo derecho
            
            #segundo caso: nodo sin hijo derecho
            elif nodo.derecho is None:
                self.__tamanno -= 1#decrementa el contador
                return nodo.izquierdo#reemplaza ntonces por el hijo izquierdo
            
            #tercer caso: nodo con dos hijos
            temp = self.findMinimo(nodo.derecho)#encuentra el minimo del subárbol derecho
            nodo.elemento = temp.elemento#copia el valor del mínimo
            nodo.derecho = self.eliminarNodo(temp.elemento, nodo.derecho)#elimina el nodo mínimo del subárbol derecho
        return nodo#retorna el nodo
    
    def inOrden(self, nodo: NodoABB | None, resultado: list) -> None:
        if nodo is not None:#si el nodo existe
            self.inOrden(nodo.izquierdo, resultado)#recorre el subárbol izquierdo
            resultado.append(nodo.elemento)#visita el nodo actual (agrega a la lista)
            self.inOrden(nodo.derecho, resultado)#recorre el subárbol derecho
        
    #para diccionario         
    def inserte(self, elemento: str):
        self.__raiz = self.insertarNodo(elemento, self.__raiz)#inserta recursivamente

    def borre(self, elemento: str) -> bool:
        tamannoOg = self.__tamanno#guarda tamaño antes de eliminar
        self.__raiz = self.eliminarNodo(elemento, self.__raiz)#intenta eliminar
        return self.__tamanno < tamannoOg#true si se eliminó, false sino

    def limpie(self):
        self.__raiz = None#elimina toda la estructura
        self.__tamanno = 0#reinicia contador

    def miembro(self, elemento: str) -> bool:
        return self.findNodo(elemento, self.__raiz) is not None#true si encuentra

    def imprima(self):
        print(self)#usa __str__ para imprimir

    def __str__(self) -> str:
        elementos = []#lista para almacenar elementos ordenados
        self.inOrden(self.__raiz, elementos)#recorre en orden y llena la lista
        return " -> ".join(elementos) if elementos else "ABB vacío"#formatea resultado

    def __len__(self) -> int:
        return self.__tamanno#retorna número de elementos
    
