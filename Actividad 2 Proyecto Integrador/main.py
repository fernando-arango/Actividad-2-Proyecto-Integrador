import time
from entorno_db import DatabaseOptimizationProblem
from algoritmos_busqueda import breadth_first_search, depth_first_search, a_star_search

def ejecutar_experimento(nombre, algoritmo, problema):
    inicio = time.perf_counter()
    nodo_solucion, nodos_expandidos = algoritmo(problema)
    fin = time.perf_counter()
    
    tiempo_ms = (fin - inicio) * 1000
    
    if nodo_solucion:
        costo = nodo_solucion.path_cost
        ruta = " -> ".join(nodo_solucion.solution())
        estado_final = nodo_solucion.state
    else:
        costo = "N/A"
        ruta = "Sin solución"
        estado_final = "N/A"
        
    return {
        "nombre": nombre,
        "nodos": nodos_expandidos,
        "tiempo": tiempo_ms,
        "costo": costo,
        "ruta": ruta,
        "estado_final": estado_final
    }

def main():
    # Estado inicial crítico: CPU=90%, RAM=80%, Fragmentación=8, Amenaza=2, Índices=0
    estado_inicial = (90, 80, 8, 2, 0)
    problema = DatabaseOptimizationProblem(estado_inicial)

    print("=" * 75)
    print("BENCHMARK DE ALGORITMOS DE BÚSQUEDA - AGENTE POSTGRESQL")
    print(f"Estado Inicial (CPU, RAM, Frag, Amenaza, Índices): {estado_inicial}")
    print("=" * 75)

    algoritmos = [
        ("BFS (Anchura)", breadth_first_search),
        ("DFS (Profundidad)", depth_first_search),
        ("A* (Heurística)", a_star_search)
    ]

    resultados = []
    for nombre, func in algoritmos:
        res = ejecutar_experimento(nombre, func, problema)
        resultados.append(res)

    # Imprimir tabla comparativa
    print(f"\n{'Algoritmo':<20} | {'Nodos Exp.':<12} | {'Tiempo (ms)':<14} | {'Costo g(n)':<10}")
    print("-" * 65)
    for r in resultados:
        print(f"{r['nombre']:<20} | {r['nodos']:<12} | {r['tiempo']:<14.4f} | {r['costo']:<10}")

    print("\n" + "=" * 75)
    print("DETALLE DE PLANES DE ACCIÓN ENCONTRADOS:")
    print("=" * 75)
    for r in resultados:
        print(f"\n[{r['nombre']}]")
        print(f"  Estado final alcanzado: {r['estado_final']}")
        print(f"  Secuencia de acciones : {r['ruta']}")

if __name__ == "__main__":
    main()