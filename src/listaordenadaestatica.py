from diccionario import Diccionario

class Array:
    def __init__(self, valor_inicial=None, tamaño = None):
        if not isinstance(tamaño, int) or tamaño < 0:
            raise ValueError("El tamaño debe ser un entero positivo.")
        if not isinstance(valor_inicial, list):
            self.__lista = [valor_inicial] * tamaño
            self.__tamaño = tamaño
        else:
            self.__lista = valor_inicial
            self.__tamaño = len(valor_inicial)        

    def __getitem__(self, índice):
        if not (0 <= índice < self.__tamaño):
            raise IndexError("Índice de arreglo fuera de los límites.")
        return self.__lista[índice]

    def __setitem__(self, índice, value):
        if not (0 <= índice < self.__tamaño):
            raise IndexError("Índice de arreglo fuera de los límites")
        self.__lista[índice] = value

    def __len__(self):
        return self.__tamaño

    def __repr__(self):
        return f"Array({self.__lista})"
    
    def __str__(self) -> str:
        return str(self.__lista)

class ListaOrdenadaEstática(Diccionario):
    def __init__(self, tamaño):
        # Se genera un arreglo de tamaño fijo con todos sus valores iniciales siendo 0
        self.__arreglo: Array = Array(valor_inicial=0, tamaño=tamaño)
        # Se guarda la posición del último elemento agregado a la lista De ser "None" la lista esta vacia
        self.__último: int | None = None
        # Capacidad máxima de la lista 
        self.__tamaño = tamaño 

    def __len__(self):
        # Verifica si no hay elementos en la lista, lo que haria que la cantidad de elementos es 0
        if self.__último is None:
            return 0
        else:
            #Si la cantidad de elementos es distinto de none, significa que, 
            # ya que el indica inicia en 0, hay +1 elementos en la lista
            return self.__último + 1
    
    def __getitem__(self, índice):
        # Devuelve el elemento en la posición solicitada
        if self.__último is None or not (0 <= índice <= self.__último):
            #Se verifica si el indice solicitado si esta detro de un rango posible
            raise IndexError("Índice fuera de rango.")
        return self.__arreglo[índice]

    def inserte(self, elemento):
        #Inserta un elemento en el arreglo

        if self.__último is None:
            # Si la lista esta vacía, se inserta el primer elemento
            self.__arreglo[0] = elemento
            self.__último = 0
            return
        
        if self.__último + 1 >= self.__tamaño:
            # Si la lista esta llena, no se puede insertar el elemento
            raise OverflowError("La lista está llena, no se pueden insertar más elementos.")

        # Busca la posición donde insertar, mediante un while
        i = 0
        while i <= self.__último and self.__arreglo[i] < elemento:
            i += 1

        # Desplaza los elementos a la derecha para hacer espacio
        for j in range(self.__último, i-1, -1):
            self.__arreglo[j+1] = self.__arreglo[j]

        # Se inserta el elemento en la posición
        self.__arreglo[i] = elemento
        self.__último += 1

    def borre(self, elemento) -> bool:
        # Borra un elemento, verificando si esta en la lista y devuelve un booleano
        if self.__último is None:
            return False

        # Mediante un ciclo busca al elemento
        i = 0
        while i <= self.__último and self.__arreglo[i] < elemento:
            i += 1
        
        # Si no se encuentra devuelve un "false"
        if i > self.__último or self.__arreglo[i] != elemento:
            return False

        # Desplaza a la izquierda todos los elementos después de encontrarlo
        for j in range(i, self.__último):
            self.__arreglo[j] = self.__arreglo[j+1]

        # Vacia la última casilla
        self.__arreglo[self.__último] = "0"
        self.__último -= 1

        # Si era el unico elemento, la lista pasa a estar vacía
        if self.__último < 0:
            self.__último = None
        return True

    def limpie(self):
        # Limpia la lista
        self.__último = None
        self.__arreglo = Array(valor_inicial="0", tamaño=self.__tamaño)

    def miembro(self, elemento) -> bool:
        # Busca si algún elemento ya se encuentra en la lista, devuelve un booleano
        
        # Verifica primero si la lista tiene elementos, de ser el caso devuelve "false"
        if self.__último is None:
            return False

        # Se busca al elemento mediante un ciclo, si es encontrado, devuleve "true", de lo contrario "false"
        i = 0
        while i <= self.__último and self.__arreglo[i] <= elemento:
            if self.__arreglo[i] == elemento:
                return True
            i += 1
        return False

    def imprima(self):
        # Imprime los elementos de la lista
        print(self)

    def __str__(self) -> str:
        # Convierte la lista en un string
        if self.__último is None:
            # Se verifica si tiene algun elemento, de lo contrario indica que se encuentra vacía
            return "Lista vacía"
        else:
            return str(self.__arreglo)
    
    def __del__(self):
        pass