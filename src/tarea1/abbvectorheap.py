from tarea1.diccionario import Diccionario

class ABBVectorHeap(Diccionario):
    def __init__(self, capacidad=100):
        self.__capacidad = capacidad#tamaño máx. del array
        self.__array = [None] * capacidad#crea array de 'capacidad' posiciones con None
        self.__tamanno = 0#contador de elementos actuales en el árbol
        
    def __indice_izquierdo(self, indice: int) -> int:
        return 2 * indice + 1#fórmula para calc. hijo izquierdo en heap

    def __indice_derecho(self, indice: int) -> int:
        return 2 * indice + 2#fórmula para calc. hijo derecho en heap

    def __indice_padre(self, indice: int) -> int:
        return (indice - 1) // 2#fórmula para calc. padre en heap

    def insertarRecursivo(self, elemento: str, indice: int) -> bool:
        self.__asegurar_capacidad(indice)#asegura que el array tenga capacidad suficiente
        
        if self.__array [indice] is None:#si posición=vacía
            self.__array[indice] = elemento#inserto elemento
            self.__tamanno += 1#incrementa contador
            return True#hooray inserto exitoso
        
        if elemento == self.__array[indice]:#si elemento ya existe
            return False#no inserta duplicados
        
        if elemento < self.__array [indice]:#si elemento es menor que actual
            #intenta insertar en hijo izquierdo
            izq =self.__indice_izquierdo(indice)
            return self.insertarRecursivo(elemento,izq)
        else:
            der = self.__indice_derecho(indice)
            return self.insertarRecursivo(elemento,der)
        

    def findRecursivo(self, elemento: str, indice: int) -> bool:
        #si índice fuera de rango o posic.vacía
        if indice >= self.__capacidad or self.__array[indice] is None:
            return False#elemento notFound
        
        if elemento == self.__array [indice]:#si encuentra elemento
            return True#elemento ya existe
        elif elemento < self.__array[indice]:#si elemento es menor
            #busca en subárbol izquierdo
            return self.findRecursivo(elemento, self.__indice_izquierdo(indice))
        else:#si elemento es mayor
            #busca en subárbol derecho
            return self.findRecursivo(elemento, self.__indice_derecho(indice))
        
    def findMinimo(self, indice: int) -> int:
        actual = indice#comienza desde el nodo que se le pasa
        izquierdo = self.__indice_izquierdo(actual)#calcula hijo izquierdo
        
        #mientras haya hijo izquierdo y no salga del array
        while izquierdo < self.__capacidad and self.__array [izquierdo] is not None:
            actual = izquierdo#baja al hijo izquierdo
            izquierdo = self.__indice_izquierdo(actual)#calcula new hijo izquierdo
        
        return actual#retorna indice del nodo minimo

    def eliminarRecursivo(self, elemento: str, indice: int) -> bool:
        #si indice fuera de rango o pos.vacía
        if indice >= self.__capacidad or self.__array[indice] is None:
            return False#elemento no encontrado
        
        if elemento < self.__array[indice]:#si elemento es menor
            #busca en subárbol izquierdo
            return self.eliminarRecursivo(elemento, self.__indice_izquierdo(indice))
        elif elemento > self.__array[indice]:#si elemento es mayor
            #busca en subárbol derecho
            return self.eliminarRecursivo(elemento, self.__indice_derecho(indice))
        
        else:#elemento found
            
            #caso 1: sin hijos
            izq = self.__indice_izquierdo(indice)#calcula hijo izquierdo
            der = self.__indice_derecho(indice)#calcula hijo derecho
            
            sin_izq= (izq >= self.__capacidad or self.__array[izq] is None)#verifica si no hay hijo izquierdo
            sin_der= (der >= self.__capacidad or self.__array[der] is None)#verifica si no hay hijo derecho
            
            #sin hijos
            if sin_izq and sin_der:
                self.__array[indice] = None#vacía la posición
                
            #solo hijo derecho
            elif sin_izq:
                self.__array[indice] = self.__array[der]#reemplaza con hijo derecho
                #elimina recursivamente el hijo derecho duped
                self.eliminarRecursivo(self.__array[der], der)
                
            #solo hijo izquierdo
            elif not sin_izq and sin_der:
                self.__array[indice] = self.__array[izq]#reemplaza con hijo izquierdo
                #elimina recursivamente el hijo izquierdo duped
                self.eliminarRecursivo(self.__array[izq], izq)
            
            else:
                min_indice = self.findMinimo(der)#encuentra el mínimo del subárbol derecho
                self.__array[indice] = self.__array[min_indice]#reemplaza con el mínimo
                self.eliminarRecursivo(self.__array[min_indice], min_indice)#elimina nodo mínimo duped
                
            return True#eliminación success
        
    def inOrdenRecursivo(self, indice: int, resultado: list) -> None:
        #si índice válido y la posición no vacía
        if indice < self.__capacidad and self.__array[indice] is not None:
            #recorre subárbol izquierdo
            self.inOrdenRecursivo(self.__indice_izquierdo(indice), resultado)
            resultado.append(self.__array[indice])  # Visita nodo actual
            #recorre subárbol derecho
            self.inOrdenRecursivo(self.__indice_derecho(indice), resultado)
            
    def __asegurar_capacidad(self, indice: int):#si el índice se sale del tamaño actual, expandimos el arreglo
        if indice >= self.__capacidad:#si índice fuera de rango
            nueva_capacidad = max(self.__capacidad * 2, indice + 1)#duplica capacidad o ajusta 
            self.__array.extend([None] * (nueva_capacidad - self.__capacidad))#extiende array con None
            self.__capacidad = nueva_capacidad#actualiza capacidad

            
    #para diccionario
            
    def inserte(self, elemento: str):
        if self.miembro(elemento):#si elemento ya existe
            print(f"'{elemento}' ya existe en el árbol.")
            return#no inserta duplicados
        if self.__tamanno == 0:#si árbol=vacío
            self.__array[0] = elemento#inserta en la raíz (pos. 0)
            self.__tamanno += 1#incrementa contador
        else:#si ya hay elementos
            if not self.insertarRecursivo(elemento, 0):#intenta insertar desde raíz
                print("No se pudo insertar: capacidad del árbol excedida.")

    def borre(self, elemento: str) -> bool:
        if self.eliminarRecursivo(elemento, 0):#elimina desde raíz
            self.__tamanno -= 1#decrementa contador
            return True#eliminación success

    def limpie(self):
        self.__array = [None] * self.__capacidad#reset todo el array a None
        self.__tamanno = 0 #reset contador

    def miembro(self, elemento: str) -> bool:
        return self.findRecursivo(elemento, 0)#busca desde raíz

    def imprima(self):
        print(self)#usa __str__ para imprimir

    def __str__(self) -> str:
        elementos = []#lista almacena elementos ordenados
        self.inOrdenRecursivo(0, elementos)#recorre en orden desde raíz
        if not elementos:
            return "ABB Vector vacío"
        return f"{' -> '.join(elementos)}"
    
    def __len__(self) -> int:
        return self.__tamanno#retorna número de elementos