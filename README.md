# Algorithmic Search Engine

Motor de búsqueda y ranking en memoria escrito en **Python puro** (sin dependencias externas), diseñado para indexar registros, filtrar por categoría y rango de precio, puntuar coincidencias y extraer los mejores *Top-K* resultados usando estructuras de datos de la librería estándar (`dict`, `set`, `heapq`).

## Arquitectura y módulos

- `engine/indexer.py`: normalización de texto/etiquetas (`normalize_token`) y clase `SearchIndex` con índice invertido (`dict` + `set`), índice por categoría y filtrado por precio.
- `engine/query.py`: cálculo de relevancia (`score_record`) y búsqueda con selección *Top-K* (`search_and_rank` usando `heapq.nlargest` y criterios de desempate).
- `engine/benchmark.py`: generación reproducible de datos sintéticos (`generate_sample_records`) y medición de tiempos de indexación y consulta con `time.perf_counter()` (`run_benchmark`).
- `engine/__init__.py`: exportación limpia de las clases y funciones principales del paquete.
- `main.py`: ejecución de ejemplo sobre un catálogo base, *benchmark* de 20,000 registros y salida detallada por consola.

## Tecnologías utilizadas

- Python 3 (librería estándar: `collections`, `re`, `heapq`, `random`, `time`, `logging`, `typing`).

## Ejecución

Abre el proyecto en **Visual Studio** y ejecuta `main.py` para ver la búsqueda de prueba, los tiempos del *benchmark* y los resultados *Top-K* en consola.
