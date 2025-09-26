from tarea1.diccionario import Diccionario

class Nodo:
    def __init__(self, elemento:str=''):#constructor, se ejecuta al crear un nodo
        self.elemento = elemento #guarda la palabra
        self.siguiente: Nodo | None = None #flecha al siguiente nodo
        
    def __str__(self) -> str:
        return f"{self.elemento}"#lo imprime más bonito

class ListaOrdenadaDinámica(Diccionario):
    def __init__(self):
        self.__cabeza = Nodo()
        self.__tamaño = 0

    def __len__(self):
        return self.__tamaño
    
    def __getitem__(self, indice):
        pass

    def inserte(self, elemento):
        referencia: Nodo = self.__cabeza
        nodo = Nodo(elemento)
        if referencia.siguiente is None:
            referencia.siguiente = nodo
        else:
            while referencia.siguiente.siguiente is not None and elemento > referencia.siguiente.elemento:
                referencia = referencia.siguiente
            nodo.siguiente = referencia.siguiente
            referencia.siguiente = nodo

    def borre(self, elemento):
        pass

    def limpie(self):
        pass

    def miembro(self, elemento: str) -> bool:
        actual = self.__cabeza.siguiente #empieza en el primer nodo real
        
        while actual is not None:#verifica que sí haya un elemento que revisar  
            if actual.elemento == elemento:#si el elemento en el que está encima sí es el que buscaba
                return True#lo encontró
            if actual.elemento > elemento:#si el elemento en el que está encima ya es mayor al que busca
                return False#no lo va a encontrar
            actual = actual.siguiente#siguiente nodo, hasta que llegue a None
        return False#llegó al final y no lo encontró

    def imprima(self):
        print(self)

    def __str__(self) -> str:
        pass
    
    def __del__(self):
        pass
    
    
    
    # 🧪 PRUEBA RÁPIDA - luego la borramos
if __name__ == "__main__":
    print("=== PRUEBA LISTA DINÁMICA ===")
    
    # Crear lista
    lista = ListaOrdenadaDinámica()
    print("Lista creada. Tamaño:", len(lista))
    
    # Insertar algunos elementos (usamos el método existente)
    lista.inserte("banana")
    lista.inserte("apple")
    lista.inserte("cherry")
    print("Elementos insertados: apple, banana, cherry")
    print("Tamaño actual:", len(lista))
    
    print("\n--- Probando búsquedas ---")
    
    # Buscar elementos que SÍ existen
    print("¿Existe 'apple'?", lista.miembro("apple"))
    print("¿Existe 'banana'?", lista.miembro("banana")) 
    print("¿Existe 'cherry'?", lista.miembro("cherry"))
    
    # Buscar elementos que NO existen
    print("¿Existe 'zebra'?", lista.miembro("zebra"))
    print("¿Existe 'ant'?", lista.miembro("ant"))
    print("¿Existe 'dog'?", lista.miembro("dog"))
    
    print("\n--- Probando caso especial ---")
    # Buscar palabra que debería estar entre apple y banana
    print("¿Existe 'apricot'?", lista.miembro("apricot"))