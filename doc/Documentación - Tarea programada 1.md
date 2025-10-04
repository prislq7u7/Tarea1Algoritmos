# Documentación Tarea Programada 1

Universidad de Costa Rica  
Escuela de Ciencias de la Computación e Informática 
CI-0116 Análisis de algoritmos y estructuras de datos - 005
Tarea programada 1
 
Profesor: Braulio Solano Rojas

Autores: 
*Karol Valeria Bolaños Sánchez, C31205*  
*Priscilla López Quesada, C14301*

**Para ejecutar:**
-   Se ejecuta con el comando "uv run tarea1", debe estar ubicado en la dirección "...\Tarea1Algoritmos" al ingresar el comando.

**Modelo Diccionario**  

El Modelo Diccionario es una clase abstracta que permite almacenar y manipular datos tipo *string* (máximo 20 caracteres, letras `a-z`).  
Las operaciones en el modelo son:  

- Init: inicializa un diccionario vacío.  
- Done: libera la memoria utilizada por el diccionario.  
- Clear: elimina todos los elementos del diccionario.  
- Insert: inserta un elemento (aunque ya exista).  
- Delete: elimina un elemento si está presente.  
- Member: consulta si un elemento pertenece al diccionario.  
- Print: imprime el contenido del diccionario.  

Este modelo es la base de nuestra implementación utilizando diversas estructuras de datos.

---

**Lista Ordenada Dinámica (por punteros)**  

Implementada como una lista simplemente enlazada:  

- Cada nodo contiene un elemento y una referencia al siguiente.  
- La inserción se realiza recorriendo la lista hasta encontrar la posición correcta.  
- La eliminación ajusta los enlaces de los nodos.  
- El tamaño se ajusta dinámicamente según el número de elementos.  

Ventajas: memoria ajustable
Limitaciones: el acceso a posiciones intermedias es lineal (O(n)).  

---

**Lista Ordenada Estática (por arreglos)**

Implementada con un arreglo de tamaño fijo:  

- Los elementos se almacenan en posiciones contiguas del arreglo.  
- La inserción y eliminación requieren desplazar elementos.  
- El acceso a cualquier posición es inmediato (O(1)).  

Ventajas: acceso rápido por índice.  
Limitaciones: tamaño fijo y posible desperdicio de memoria. 

---

**Tabla Hash**  
Implementada usando **encadenamiento** para manejar colisiones:

- Arreglo de listas ordenadas (buckets)
- Cada bucket es una ListaOrdenadaDinámica
- Cuando el factor de carga ≥ 0.7, la capacidad se duplica

Función Hash (__funcion_hash()): 
    ¿Qué hace?
    - Convierte un string en un número entero que corresponde al índice de un bucket en la tabla.
    - Multiplica el acumulador val_hash por 31 (un número primo que se usa para las tablas hash para que distribuya uniformemente los valores), suma el valor ASCII de c/u char, y luego toma el módulo sobre la capacidad de la tabla, lo que hace que los elementos se repartan entre los buckets disponibles.

Redistribución:
    - Se da en la función __redimensionar(), cuando el (número de elementos / número de buckets) supera la carga máxima de la tabla, se duplica su capacidad. Se crea un nuevo arreglo de buckets vacíos con la nueva capacidad, a los elementos antiguos se les aplica la __funcion_hash() de nuevo y se reinsertan en los nuevos buckets.
    - El proceso de "redistribución" lo evaluamos en O(n) porque hay que recorrer todos los elementos e insertarlos de nuevo, pero solo ocurre cuando se excede el factor de carga máxima, por lo que no debe hacerse en cada corrida, así que en el mejor caso es O(1).


---

El programa principal ofrece un menú interactivo para realizar operaciones sobre el Diccionario con distintas implementaciones.  
Permite:  

* Seleccionar la estructura de datos (Lista Ordenada Dinámica, Estática o Hash).  
* Insertar, borrar, verificar existencia, imprimir y limpiar elementos.  
* Salir del sistema.  

El menú utiliza la librería *Rich* para mostrar paneles coloridos y mejorar la interacción en consola.  

---

## Estado de Avance 1

En esta primera etapa, hemos implementado y probado:  

- Diccionario con *Lista Ordenada Dinámica*.  
- Diccionario con *Lista Ordenada Estática* .
- Diccionario con *Tabla Hash Abierta*.  
- Programa de prueba con menú de opciones.  