# Documentación Tarea Programada 1

Universidad de Costa Rica  
Escuela de Ciencias de la Computación e Informática 
CI-0116 Análisis de algoritmos y estructuras de datos - 005
Tarea programada 1
 
Profesor: Braulio Solano Rojas

Autores: 
*Karol Valeria Bolaños Sánchez, C31205*  
*Priscilla*

**El programa se ejecuta con el comando "uv run tarea1"**

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