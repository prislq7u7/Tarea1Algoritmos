from tarea1.diccionario import Diccionario
from tarea1.listaordenadadinamica import ListaOrdenadaDinámica
from tarea1.listaordenadaestatica import ListaOrdenadaEstática
from tarea1.tablahashabierta import TablaHashAbierta
from tarea1.abbpunteros import ABBPunteros
from tarea1.abbvectorheap import ABBVectorHeap
from tarea1.triepunteros import TriePunteros
from tarea1.triearreglos import TrieArreglos

import time
import random
import string
import sys
import os
from typing import Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import gc
#se debe instalar matplotlib para generar gráficos

#detecta si matplotlib está disponible para crear gráficos
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_DISPONIBLE = True
except ImportError:
    MATPLOTLIB_DISPONIBLE = False

def medir_memoria_objeto(obj: Any) -> int:
    #mide la memoria de manera recursiva
    def _get_size(obj: Any, seen: set = None) -> int:
        #si es la primera llamada, inicializa
        if seen is None:
            seen = set()
        
        #evita ciclos infinitos
        obj_id = id(obj)
        if obj_id in seen:
            return 0
        
        #marca objeto como visitado
        seen.add(obj_id)
        
        #obtiene el tamaño del objeto
        size = sys.getsizeof(obj)
        
        #si es un diccionario, suma el tamaño de claves y valores
        if isinstance(obj, dict):
            size += sum(_get_size(k, seen) + _get_size(v, seen) for k, v in obj.items())
        #si es una colección, suma el tamaño de todos sus elementos
        elif isinstance(obj, (list, tuple, set, frozenset)):
            size += sum(_get_size(item, seen) for item in obj)
        #si tiene atributos procesa
        elif hasattr(obj, '__dict__'):
            size += _get_size(obj.__dict__, seen)
        #procesa los atributos definidos en slots
        elif hasattr(obj, '__slots__'):
            for slot in obj.__slots__:
                if hasattr(obj, slot):
                    size += _get_size(getattr(obj, slot), seen)
        
        return size
    
    return _get_size(obj)

class Rendimiento:
    
    def __init__(self):
        #inicializa la clase con tamaños de prueba
        self.tamanos = [100, 5000, 20000]
        #número de repeticiones para cada prueba
        self.repeticiones = 10
        self.console = Console()
        
        #crear carpeta para gráficos si no existe y matplotlib está disponible
        if MATPLOTLIB_DISPONIBLE and not os.path.exists("graficos"):
            os.makedirs("graficos")
    
    def generar_nombre_unico(self, base_nombre, extension="png"):
        #genera un nombre de archivo único para no sobreescribir
        nombre = f"{base_nombre}.{extension}"
        contador = 1
        
        #si archivo ya existe buscar un nombre único (1), (2)...
        while os.path.exists(os.path.join("graficos", nombre)):
            nombre = f"{base_nombre} ({contador}).{extension}"
            contador += 1##aunmenta el contador hasta encontrar un nombre libre
        
        return nombre
    
    def generar_palabras(self, n: int) -> list:
        #genera una lista de palabras rand para las pruebas
        return [''.join(random.choices(string.ascii_lowercase, k=20)) 
                for _ in range(n)]
    
    def medir_operaciones(self, dicc, palabras):
        #mide los tiempos de todas las operaciones 
        tiempos = {}
        
        #fuerza garbage collection antes de medir para obtener mediciones limpias
        gc.collect()
        
        #mide la memoria antes de las operaciones 
        memoria_inicial = medir_memoria_objeto(dicc)
        
        #mide insercion
        start = time.perf_counter() 
        for palabra in palabras:
            dicc.inserte(palabra) #inserta las palabras
        tiempos['insercion'] = time.perf_counter() - start
        
        #medición de búsqueda
        start = time.perf_counter()
        #busca solo las primeras 50 palabras
        for palabra in palabras[:50]:
            dicc.miembro(palabra)
        tiempos['busqueda'] = time.perf_counter() - start
        
        #medición de borrado
        start = time.perf_counter()
        #borra solo las primeras 30 palabras
        for palabra in palabras[:30]:
            dicc.borre(palabra)
        tiempos['borrado'] = time.perf_counter() - start
        
        #medición de print
        start = time.perf_counter()
        str_repr = str(dicc)  #simula operación print convirtiendo a string
        tiempos['print'] = time.perf_counter() - start
        
        #medición de done
        start = time.perf_counter()
        dicc.limpie() #limpia el diccionario
        tiempos['done'] = time.perf_counter() - start
        
        #mide la memoria despues de las operaciones
        memoria_final = medir_memoria_objeto(dicc)
        tiempos['memoria'] = memoria_final #memoria base de la estructura
        
        return tiempos
    
    def medir_memoria_estructura(self, constructor, tamanno: int) -> int:
        
        #Forza a garbage collection
        gc.collect()
        
        #crea nueva instancia y generar palabras de prueba
        dicc = constructor()
        palabras = self.generar_palabras(tamanno)
        
        #mide memoria inicial
        memoria_inicial = medir_memoria_objeto(dicc)
        
        #inserta todos los elementos
        for palabra in palabras:
            dicc.inserte(palabra)
        
        #mide memoria con todos los elementos insertados
        memoria_con_elementos = medir_memoria_objeto(dicc)
        
        #calcula memoria usada por los elementos
        memoria_usada = memoria_con_elementos - memoria_inicial
        
        #limpia la estructura
        dicc.limpie()
        
        return memoria_usada
    
    def probar_estructura(self, constructor, tamanno):
        
        #listas para almacenar resultados de cada repeti.
        tiempos_insercion = []
        tiempos_busqueda = []
        tiempos_borrado = []
        tiempos_print = []
        tiempos_done = []
        memoria_usada = []
        
        #hace varias repeticiones para obtener promedio
        for _ in range(self.repeticiones):
            #limpia memoria antes de cada prueba
            gc.collect()
            
            #crea una nueva instancia y genera palabras
            dicc = constructor()
            palabras = self.generar_palabras(tamanno)
            
            #mide todas las operaciones
            tiempos = self.medir_operaciones(dicc, palabras)
            
            #almacena resultados de esta repetición
            tiempos_insercion.append(tiempos['insercion'])
            tiempos_busqueda.append(tiempos['busqueda'])
            tiempos_borrado.append(tiempos['borrado'])
            tiempos_print.append(tiempos['print'])
            tiempos_done.append(tiempos['done'])
            memoria_usada.append(tiempos['memoria'])
            
            #limpia y libera memoria
            dicc.limpie()
            del dicc
            gc.collect()
        
        #retorna promedios de todas las repeticiones
        return {
            'insercion': sum(tiempos_insercion) / len(tiempos_insercion),
            'busqueda': sum(tiempos_busqueda) / len(tiempos_busqueda),
            'borrado': sum(tiempos_borrado) / len(tiempos_borrado),
            'print': sum(tiempos_print) / len(tiempos_print),
            'done': sum(tiempos_done) / len(tiempos_done),
            'memoria': sum(memoria_usada) / len(memoria_usada)
        }
    
    def crear_grafico_comparacion(self, nombre1, nombre2, resultados1, resultados2, titulo, num_comparacion):
        
        #si matplotlib no está instalado, usa gráficos de texto
        if not MATPLOTLIB_DISPONIBLE:
            self.crear_grafico_texto(nombre1, nombre2, resultados1, resultados2, titulo)
            return None
        
        try:
            # Crear figura con subgráficos (2 filas, 3 columnas)
            plt.figure(figsize=(15, 10))
            
            # Definir operaciones a graficar
            operaciones = ['insercion', 'busqueda', 'borrado', 'print', 'done']
            nombres_ops = ['Inserción', 'Búsqueda', 'Borrado', 'Print', 'Done']
            colores = ['blue', 'green', 'red', 'orange', 'purple']
            
            # Crea un subgráfico para cada operación
            for i, (op, nombre_op, color) in enumerate(zip(operaciones, nombres_ops, colores)):
                plt.subplot(2, 3, i + 1)  # Posición en la cuadrícula 2x3
                
                # Obtiene tiempos para ambos estructuras en todos los tamaños
                tiempos1 = [resultados1[tam][op] for tam in self.tamanos]
                tiempos2 = [resultados2[tam][op] for tam in self.tamanos]
                
                # Configura posiciones para barras
                x_pos = range(len(self.tamanos))
                width = 0.35  # Ancho de las barras
                
                # Crea barras para ambas estructuras
                plt.bar([p - width/2 for p in x_pos], tiempos1, width, 
                       label=nombre1, color=color, alpha=0.7)
                plt.bar([p + width/2 for p in x_pos], tiempos2, width, 
                       label=nombre2, color=color, alpha=0.4)
                
                # Configura etiquetas y estilo
                plt.xlabel('Tamaño del Diccionario')
                plt.ylabel('Tiempo (segundos)')
                plt.title(f'Tiempo de {nombre_op}')
                plt.xticks(x_pos, [f'{tam:,}' for tam in self.tamanos])
                plt.legend()
                plt.grid(True, alpha=0.3)
        
            plt.subplot(2, 3, 6)
            # Convierte memoria de bytes a KB
            memoria1 = [resultados1[tam]['memoria'] / 1024 for tam in self.tamanos]
            memoria2 = [resultados2[tam]['memoria'] / 1024 for tam in self.tamanos]
            
            x_pos = range(len(self.tamanos))
            width = 0.35
            
            # Barras para comparación de memoria
            plt.bar([p - width/2 for p in x_pos], memoria1, width, 
                   label=nombre1, color='brown', alpha=0.7)
            plt.bar([p + width/2 for p in x_pos], memoria2, width, 
                   label=nombre2, color='brown', alpha=0.4)
            
            plt.xlabel('Tamaño del Diccionario')
            plt.ylabel('Memoria (KB)')
            plt.title('Uso de Memoria Base')
            plt.xticks(x_pos, [f'{tam:,}' for tam in self.tamanos])
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Ajustar layout y agregar título principal
            plt.tight_layout()
            plt.suptitle(f'{titulo}\nComparación {num_comparacion}', 
                        fontsize=14, fontweight='bold')
            plt.subplots_adjust(top=0.92)
            
            # Genera un nombre único y guarda el gráfico
            base_nombre = f"comparacion_{num_comparacion}_{nombre1}_vs_{nombre2}"
            nombre_archivo = self.generar_nombre_unico(base_nombre)
            ruta_completa = os.path.join("graficos", nombre_archivo)
            
            plt.savefig(ruta_completa, dpi=300, bbox_inches='tight')
            plt.close()
            
            return nombre_archivo
            
        except Exception as e:
            # En caso de error, usa gráficos de texto.
            self.console.print(f"[red]Error creando gráfico: {e}[/]")
            self.crear_grafico_texto(nombre1, nombre2, resultados1, resultados2, titulo)
            return None
            
        
    
    def crear_grafico_tendencias(self, nombre1, nombre2, resultados1, resultados2, titulo, num_comparacion):
        # Crea gráfico de tendencias para ver crecimiento.
        
        if not MATPLOTLIB_DISPONIBLE:
            return None
        
        try:
            plt.figure(figsize=(12, 8))
            
            # Operaciones principales para análisis de tendencias
            operaciones = ['insercion', 'busqueda', 'borrado']
            nombres_ops = ['Inserción', 'Búsqueda', 'Borrado']
            # Separa marcadores y estilos de línea
            marcadores = ['o', 's', '^']  # Marcadores para cada operación
            estilos_linea = ['-', '--', '-.']  # Estilos de línea para cada operación
            colores = ['blue', 'green', 'red']
        
            # Grafica cada operación para ambas estructuras
            for op, nombre_op, marcador, estilo, color in zip(operaciones, nombres_ops, marcadores, estilos_linea, colores):
                tiempos1 = [resultados1[tam][op] for tam in self.tamanos]
                tiempos2 = [resultados2[tam][op] for tam in self.tamanos]
                
                # Línea sólida para estructura 1, punteada para estructura 2
                plt.plot(self.tamanos, tiempos1, 
                        marker=marcador, linestyle=estilo,
                        label=f'{nombre1} - {nombre_op}', 
                        linewidth=2, markersize=6, color=color)
                plt.plot(self.tamanos, tiempos2, 
                        marker=marcador, linestyle=':',  
                        label=f'{nombre2} - {nombre_op}', 
                        linewidth=2, markersize=6, color=color, alpha=0.7)
            
            # Usar escalas logarítmicas para mejor visualización de magnitud
            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('Tamaño del Diccionario (N) - Escala Logarítmica')
            plt.ylabel('Tiempo (segundos) - Escala Logarítmica')
            plt.title(f'Tendencias de Rendimiento\n{titulo}')
            plt.legend()
            plt.grid(True, which="both", ls="--", alpha=0.5)
            
            # Guardar gráfico
            base_nombre = f"tendencias_{num_comparacion}_{nombre1}_vs_{nombre2}"
            nombre_archivo = self.generar_nombre_unico(base_nombre)
            ruta_completa = os.path.join("graficos", nombre_archivo)
            
            plt.savefig(ruta_completa, dpi=300, bbox_inches='tight')
            plt.close()
            
            return nombre_archivo
            
        except Exception as e:
            self.console.print(f"[red]Error creando gráfico de tendencias: {e}[/]")
            return None
    
    def crear_grafico_memoria(self, nombre1, nombre2, resultados1, resultados2, titulo, num_comparacion):
        
        # Crea gráfico específico para comparación de memoria.
        
        if not MATPLOTLIB_DISPONIBLE:
            return None
        
        try:
            plt.figure(figsize=(10, 6))
            
            # Convertir memoria de bytes a MB
            memoria1 = [resultados1[tam]['memoria'] / (1024 * 1024) for tam in self.tamanos]
            memoria2 = [resultados2[tam]['memoria'] / (1024 * 1024) for tam in self.tamanos]
            
            x_pos = range(len(self.tamanos))
            width = 0.35
            
            # Barras para memoria
            plt.bar([p - width/2 for p in x_pos], memoria1, width, 
                   label=nombre1, color='teal', alpha=0.7)
            plt.bar([p + width/2 for p in x_pos], memoria2, width, 
                   label=nombre2, color='teal', alpha=0.4)
            
            plt.xlabel('Tamaño del Diccionario')
            plt.ylabel('Memoria (MB)')
            plt.title(f'Comparación de Memoria Base\n{titulo}')
            plt.xticks(x_pos, [f'{tam:,}' for tam in self.tamanos])
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Guarda gráfico
            base_nombre = f"memoria_{num_comparacion}_{nombre1}_vs_{nombre2}"
            nombre_archivo = self.generar_nombre_unico(base_nombre)
            ruta_completa = os.path.join("graficos", nombre_archivo)
            
            plt.savefig(ruta_completa, dpi=300, bbox_inches='tight')
            plt.close()
            
            return nombre_archivo
            
        except Exception as e:
            self.console.print(f"[red]Error creando gráfico de memoria: {e}[/]")
            return None
    
    def crear_grafico_texto(self, nombre1, nombre2, resultados1, resultados2, titulo):
        
        # Crea gráficos ASCII como fallback cuando matplotlib no está disponible.
        
        self.console.print()
        self.console.print(Panel(f" GRÁFICOS ASCII - {titulo}", style="bold yellow"))
        
        # Gráfico de barras ASCII para inserción
        self.console.print("\n Tiempos de Inserción:")
        for tam in self.tamanos:
            tiempo1 = resultados1[tam]['insercion']
            tiempo2 = resultados2[tam]['insercion']
            
            # Calcular anchos de barras relativos
            max_bar_width = 40
            max_tiempo = max(tiempo1, tiempo2)
            bar1_width = int((tiempo1 / max_tiempo) * max_bar_width) if max_tiempo > 0 else 0
            bar2_width = int((tiempo2 / max_tiempo) * max_bar_width) if max_tiempo > 0 else 0
            
            # Mostrar barras ASCII
            self.console.print(f"  N={tam:,}:")
            self.console.print(f"    {nombre1}: {'█' * bar1_width} {tiempo1:.4f}s")
            self.console.print(f"    {nombre2}: {'█' * bar2_width} {tiempo2:.4f}s")
        
        # Gráfico de memoria ASCII
        self.console.print("\n Memoria Base:")
        for tam in self.tamanos:
            mem1 = resultados1[tam]['memoria'] / 1024  # Convertir a KB
            mem2 = resultados2[tam]['memoria'] / 1024
            
            max_bar_width = 30
            max_mem = max(mem1, mem2)
            bar1_width = int((mem1 / max_mem) * max_bar_width) if max_mem > 0 else 0
            bar2_width = int((mem2 / max_mem) * max_bar_width) if max_mem > 0 else 0
            
            self.console.print(f"  N={tam:,}:")
            self.console.print(f"    {nombre1}: {'█' * bar1_width} {mem1:.1f} KB")
            self.console.print(f"    {nombre2}: {'█' * bar2_width} {mem2:.1f} KB")
    
    def comparar_estructuras(self, nombre1, constructor1, nombre2, constructor2, titulo, num_comparacion):
        
        # Función para comparar dos estructuras de datos.
        self.console.print()
        self.console.print(Panel(f" COMPARACIÓN {num_comparacion}: {titulo}", style="bold blue"))
        
        # Advertencia si matplotlib no está disponible
        if not MATPLOTLIB_DISPONIBLE:
            self.console.print("[yellow]  Matplotlib no disponible. Usando gráficos ASCII...[/]")
        
        # Crear tabla para mostrar resultados
        tabla = Table(show_header=True, header_style="bold magenta")
        tabla.add_column("Tamaño", style="cyan", width=12)
        tabla.add_column("Operación", style="white", width=15)
        tabla.add_column(nombre1, justify="center", width=18)
        tabla.add_column(nombre2, justify="center", width=18)
        tabla.add_column("Ganador", justify="center", width=15)
        
        # Diccionarios para almacenar resultados
        resultados1 = {}
        resultados2 = {}
        
        # Prueba para cada tamaño de diccionario
        for tam in self.tamanos:
            self.console.print(f"Probando {tam} elementos...")
            
            # Prueba ambas estructuras
            resultados1[tam] = self.probar_estructura(constructor1, tam)
            resultados2[tam] = self.probar_estructura(constructor2, tam)
            
            # Define operaciones a mostrar en tabla
            operaciones = [
                ('insercion', 'Inserción'),
                ('busqueda', 'Búsqueda'), 
                ('borrado', 'Borrado'),
                ('print', 'Print'),
                ('done', 'Done'),
                ('memoria', 'Memoria')
            ]
            
            # Agrega filas a la tabla para cada operación
            for op_key, op_nombre in operaciones:
                val1 = resultados1[tam][op_key]
                val2 = resultados2[tam][op_key]
                
                # Determina ganador
                if val1 < val2:
                    ganador = f"[green]{nombre1}[/]"
                    diferencia = f"({val2/val1:.1f}x)" if val1 > 0 else ""
                elif val2 < val1:
                    ganador = f"[green]{nombre2}[/]"
                    diferencia = f"({val1/val2:.1f}x)" if val2 > 0 else ""
                else:
                    ganador = "[yellow]Empate[/]"
                    diferencia = ""
                
                # Formatear valores según el tipo de operación
                if op_key == 'memoria':
                    if val1 > 1024 * 1024:  # MB
                        fmt_val1 = f"{val1/(1024*1024):.1f} MB"
                        fmt_val2 = f"{val2/(1024*1024):.1f} MB"
                    elif val1 > 1024:  # KB
                        fmt_val1 = f"{val1/1024:.1f} KB"
                        fmt_val2 = f"{val2/1024:.1f} KB"
                    else:  # Bytes
                        fmt_val1 = f"{val1:,.0f} B"
                        fmt_val2 = f"{val2:,.0f} B"
                else:
                    #formatea tiempos
                    fmt_val1 = f"{val1:.4f}s"
                    fmt_val2 = f"{val2:.4f}s"
                
                #agrega fila a la tabla
                tabla.add_row(
                    f"{tam:,}" if op_key == 'insercion' else "",  # Mostrar tamaño solo en primera fila
                    op_nombre,
                    fmt_val1,
                    fmt_val2,
                    f"{ganador} {diferencia}"
                )
            
            #agregar separador entre tamaños
            if tam != self.tamanos[-1]:
                tabla.add_row("─" * 12, "─" * 15, "─" * 18, "─" * 18, "─" * 15)
        
        #mostrar tabla completa
        self.console.print(tabla)
        
        #crea gráficos visuales
        archivos_guardados = []
        
        if MATPLOTLIB_DISPONIBLE:
            self.console.print("\n Generando gráficos...")
            
            #crea diferentes tipos de gráficos
            archivo1 = self.crear_grafico_comparacion(nombre1, nombre2, resultados1, resultados2, titulo, num_comparacion)
            if archivo1:
                archivos_guardados.append(archivo1)
                self.console.print(f"   [green]Gráfico de comparación: {archivo1}[/]")
            
            archivo2 = self.crear_grafico_tendencias(nombre1, nombre2, resultados1, resultados2, titulo, num_comparacion)
            if archivo2:
                archivos_guardados.append(archivo2)
                self.console.print(f"   [green]Gráfico de tendencias: {archivo2}[/]")
            
            archivo3 = self.crear_grafico_memoria(nombre1, nombre2, resultados1, resultados2, titulo, num_comparacion)
            if archivo3:
                archivos_guardados.append(archivo3)
                self.console.print(f"  [green]Gráfico de memoria: {archivo3}[/]")
        else:
            #usa gráficos ascii si matplotlib no está disponible
            self.crear_grafico_texto(nombre1, nombre2, resultados1, resultados2, titulo)
        
        #muestra resumen comparativo
        self._mostrar_resumen_comparacion(nombre1, nombre2, resultados1, resultados2)
        
        return resultados1, resultados2, archivos_guardados
    
    def _mostrar_resumen_comparacion(self, nombre1, nombre2, res1, res2):
        
        #muestra un resumen de victorias entre las comparaciones
        self.console.print()
        self.console.print(Panel("RESUMEN COMPARATIVO", style="bold green"))
        
        #cuenta victorias para cada tamaño
        for tam in self.tamanos:
            victorias1 = 0
            victorias2 = 0
            
            #comparar cada operación
            for op in ['insercion', 'busqueda', 'borrado', 'print', 'done', 'memoria']:
                if res1[tam][op] < res2[tam][op]:
                    victorias1 += 1
                elif res2[tam][op] < res1[tam][op]:
                    victorias2 += 1
            
            #mostrar resultado del enfrentamiento
            if victorias1 > victorias2:
                self.console.print(f" {tam:,} elementos: [bold green]{nombre1}[/] ({victorias1}-{victorias2})")
            elif victorias2 > victorias1:
                self.console.print(f" {tam:,} elementos: [bold green]{nombre2}[/] ({victorias2}-{victorias1})")
            else:
                self.console.print(f" {tam:,} elementos: [bold yellow]Empate[/] ({victorias1}-{victorias2})")

    def analizar_memoria_detallada(self):
        
        #análisis del uso de memoria para todas las estructuras
        self.console.print()
        self.console.print(Panel("ANÁLISIS DETALLADO DE MEMORIA", style="bold cyan"))
        
        #define todas las estructuras a analizar
        estructuras = {
            "LO_Punteros": ListaOrdenadaDinámica,
            "LO_Arreglos": lambda: ListaOrdenadaEstática(50000),
            "Tabla_Hash": TablaHashAbierta,
            "ABB_Punteros": ABBPunteros,
            "ABB_VectorHeap": ABBVectorHeap,
            "Trie_Punteros": TriePunteros,
            "Trie_Arreglos": TrieArreglos
        }
        
        #crea tabla para resultados de memoria
        tabla = Table(show_header=True, header_style="bold magenta")
        tabla.add_column("Estructura", style="cyan", width=20)
        for tam in self.tamanos:
            tabla.add_column(f"{tam:,} elem", justify="center", width=15)
        
        resultados_memoria = {}
        
        #analizar memoria para cada estructura
        for nombre, constructor in estructuras.items():
            self.console.print(f"Analizando memoria de {nombre}...")
            fila = [nombre]
            memoria_por_tamanno = {}
            
            #medir memoria para cada tamaño
            for tam in self.tamanos:
                try:
                    memoria_bytes = self.medir_memoria_estructura(constructor, tam)
                    memoria_kb = memoria_bytes / 1024
                    
                    #formatear resultado según tamaño
                    if memoria_kb > 1024: 
                        fila.append(f"{memoria_kb/1024:.1f} MB")
                    else:
                        fila.append(f"{memoria_kb:.1f} KB")
                    
                    memoria_por_tamanno[tam] = memoria_bytes
                    
                except Exception as e:
                    #manejar errores en medición
                    fila.append(f"Error")
                    memoria_por_tamanno[tam] = 0
                    self.console.print(f"[red]Error en {nombre} con {tam}: {e}[/]")
            
            #almacenar resultados y agregar a tabla
            resultados_memoria[nombre] = memoria_por_tamanno
            tabla.add_row(*fila)
        
        #mostrar tabla completa
        self.console.print(tabla)
        
        #crea gráfico comparativo de memoria si es posible
        if MATPLOTLIB_DISPONIBLE:
            try:
                plt.figure(figsize=(12, 8))
                
                colores = ['blue', 'green', 'red', 'orange', 'purple', 'brown', 'pink']
                estilos = ['o-', 's--', '^-', 'd-.', '*-', 'x-', '+-']
                
                #graficar cada estructura
                for i, (nombre, memoria_data) in enumerate(resultados_memoria.items()):
                    memoria_mb = [memoria_data[tam] / (1024 * 1024) for tam in self.tamanos]
                    plt.plot(self.tamanos, memoria_mb, estilos[i % len(estilos)], 
                            label=nombre, color=colores[i % len(colores)], 
                            linewidth=2, markersize=6)
                
                plt.xlabel('Tamaño del Diccionario')
                plt.ylabel('Memoria Utilizada (MB)')
                plt.title('Comparación de Memoria por Estructura de Datos')
                plt.legend()
                plt.grid(True, alpha=0.3)
                plt.xscale('log')  # Escala logarítmica
                
                # Guardar gráfico
                nombre_archivo = self.generar_nombre_unico("memoria_comparativa_todas_estructuras")
                ruta_completa = os.path.join("graficos", nombre_archivo)
                
                plt.savefig(ruta_completa, dpi=300, bbox_inches='tight')
                plt.close()
                
                self.console.print(f"\n [green]Gráfico de memoria comparativa guardado: {nombre_archivo}[/]")
                
            except Exception as e:
                self.console.print(f"[red]Error creando gráfico de memoria comparativa: {e}[/]")
        
        return resultados_memoria

    # Funciones de comparación

    def comparacion_1_LO_punteros_vs_arreglos(self):
        # Comparación 1: Lista Ordenada por punteros vs arreglos
        return self.comparar_estructuras(
            "LO_Punteros", 
            ListaOrdenadaDinámica,
            "LO_Arreglos", 
            lambda: ListaOrdenadaEstática(50000),  # Lambda para pasar parámetro de capacidad
            "COMPARACIÓN 1: Lista Ordenada - Punteros vs Arreglos",
            1
        )

    def comparacion_2_ABB_punteros_vs_vectorheap(self):
        # Comparación 2: ABB por punteros vs Vector Heap con tamaños especiales
        #guarda los tamaños originales para restaurarlos después
        tamanos_originales = self.tamanos.copy()
    
        #ABBVectorHeap tiene limitaciones de memoria con tamaños grandes
        self.tamanos = [100, 1500, 3000]  # Tamaños reducidos para ABBVectorHeap
    
        self.console.print("[yellow]Usando tamaños reducidos para ABBVectorHeap (100, 1500, 3000)")
    
        try:
            resultado = self.comparar_estructuras(
                "ABB_Punteros",
                ABBPunteros,
                "ABB_VectorHeap", 
                ABBVectorHeap,
                "ABB - Punteros vs Vector Heap",
                2
            )
            return resultado
        finally:
            #restaurar los tamaños originales para las siguientes comparaciones
            self.tamanos = tamanos_originales

    def comparacion_3_Trie_punteros_vs_arreglos(self):
        # Comparación 3: Trie por punteros vs arreglos
        return self.comparar_estructuras(
            "Trie_Punteros",
            TriePunteros,
            "Trie_Arreglos",
            TrieArreglos,
            "COMPARACIÓN 3: Trie - Punteros vs Arreglos",
            3
        )

    def comparacion_4_LO_punteros_vs_tablahash(self):
        # Comparación 4: Lista Ordenada vs Tabla Hash
        return self.comparar_estructuras(
            "LO_Punteros",
            ListaOrdenadaDinámica,
            "Tabla_Hash",
            TablaHashAbierta,
            "COMPARACIÓN 4: Lista Ordenada vs Tabla Hash",
            4
        )

    def comparacion_5_LO_punteros_vs_ABB_punteros(self):
        # Comparación 5: Lista Ordenada vs ABB (punteros)
        return self.comparar_estructuras(
            "LO_Punteros",
            ListaOrdenadaDinámica,
            "ABB_Punteros",
            ABBPunteros,
            "COMPARACIÓN 5: Lista Ordenada vs ABB (Punteros)",
            5
        )

    def comparacion_6_LO_punteros_vs_Trie_punteros(self):
        # Comparación 6: Lista Ordenada vs Trie (punteros)
        return self.comparar_estructuras(
            "LO_Punteros",
            ListaOrdenadaDinámica,
            "Trie_Punteros",
            TriePunteros,
            "COMPARACIÓN 6: Lista Ordenada vs Trie (Punteros)",
            6
        )

    def comparacion_7_TablaHash_vs_Trie_punteros(self):
        # Comparación 7: Tabla Hash vs Trie (punteros)
        return self.comparar_estructuras(
            "Tabla_Hash",
            TablaHashAbierta,
            "Trie_Punteros",
            TriePunteros,
            "COMPARACIÓN 7: Tabla Hash vs Trie (Punteros)",
            7
        )