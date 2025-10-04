from tarea1.diccionario import Diccionario
from tarea1.listaordenadadinamica import ListaOrdenadaDinámica #cada bucket es una lista ordenada dinámica

class TablaHashAbierta(Diccionario):#herencia de Diccionario
    
    def __init__(self, capacidad=10, carga_max=0.7):#constructor
        self.__capacidad = capacidad #número de buckets de la tabla hash
        self.__carga_max = carga_max #factor de carga máximo permitido
        self.__tamanno = 0 #cuántps elementos hay en total
        self.__buckets = [ListaOrdenadaDinámica() for F in range(capacidad)]#bucket es ubicación de memoria, crea array de listas vacías, c/u lista es un bucket
        
    def __factor_carga(self) -> float:#factor de carga = #elementos / #buckets
        return self.__tamanno / self.__capacidad
      
    def __len__(self):
        return self.__tamanno  
    
    def __funcion_hash(self, elemento: str) -> int:#función para convertir string a número para saber en qué bucket va
        val_hash = 0
        for char in elemento:
            val_hash = (val_hash * 31 + ord(char)) % self.__capacidad#ord(char) da valor ASCII
        return val_hash
    
    def inserte(self, elemento : str):
        if self.__factor_carga() >= self.__carga_max:
            self.__redimensionar(self.__capacidad * 2)#si la tabla está muy llena se duplica su tamaño
        indice_bucket = self.__funcion_hash(elemento)#calcula en qué bucket va el elemento
        bucket = self.__buckets[indice_bucket]#obtiene la lista correspondiente a ese bucket
        if not bucket.miembro(elemento):#solo inserta elem. si no existe ya
            bucket.inserte(elemento)
            self.__tamanno += 1
    
    def __redimensionar(self, new_capacidad: int):
        print(f"Redimensionando tabla hash: {new_capacidad}")
        old_buckets = self.__buckets#guardar los buckets viejos
        self.__capacidad = new_capacidad#actualizar capacidad
        self.__buckets = [ListaOrdenadaDinámica() for _ in range(new_capacidad)]#crear nuevos buckets vacíos con nueva capacidad
        self.__tamanno = 0#reiniciar contador tamaño
        
        #reinserta todos los elementos en la nueva tabka
        for bucket in old_buckets:#recorrer cada bucket viejo
            elementos = []
            actual = bucket._ListaOrdenadaDinámica__cabeza.siguiente#nodo actual empieza en cabeza
            while actual is not None:#mientras haya nodos en el bucket
                elementos.append(actual.elemento)#agrega el elemento del nodo actual a la lista de elementos
                actual = actual.siguiente#avanzar al siguiente nodo
                
            for elemento in elementos:
                self.inserte(elemento)#inserta cada elemento en la nueva tabla hash
                
    def miembro(self, elemento: str) -> bool:
        indice_bucket = self.__funcion_hash(elemento)#calcula en qué bucket va el elemento (indice)
        bucket = self.__buckets[indice_bucket]#obtiene la lista correspondiente a ese bucket
        return bucket.miembro(elemento)#verifica si el elemento está en esa lista (solo en ese bucket)
    
    def borre(self, elemento: str) -> bool:
        indice_bucket = self.__funcion_hash(elemento)#calcula en qué bucket va el elemento (indice)
        bucket = self.__buckets[indice_bucket]#obtiene la lista correspondiente a ese bucket
        
        if bucket.borre(elemento):#intenta borrar el elemento en esa lista (solo en ese bucket)
            self.__tamanno -= 1#si lo borró, actualiza el tamaño (decrementa)
            return True
        return False
    
    def limpie(self):
        self.__buckets = [ListaOrdenadaDinámica() for _ in range(self.__capacidad)]#reinicia los buckets a listas vacías
        self.__tamanno = 0#reinicia el tamaño a 0
        
    def imprima(self):
        print(self)
    
    def __str__(self) -> str: #como se ve la tabla
        resultado = []
        for i, bucket in enumerate(self.__buckets):
            if len(bucket) > 0:
                resultado.append(f"Bucket {i}: [{bucket}]")#como se ve cada bucket
        return "\n".join(resultado) if resultado else "Tabla Hash Abierta vacía"
