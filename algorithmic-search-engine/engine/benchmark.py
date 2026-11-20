import random
import time
from .indexer import SearchIndex
from .query import search_and_rank

CATEGORIES = ["almacenamiento", "graficos", "memoria", "perifericos", "fuentes"]
TAG_POOL = [
    "ssd",
    "nvme",
    "1tb",
    "2tb",
    "gen4",
    "rtx",
    "gpu",
    "12gb",
    "16gb",
    "ddr5",
    "6000mhz",
    "mecanico",
    "inalambrico",
    "80plus",
    "modular",
    "rgb",
]


def generate_sample_records(count: int = 20000, seed: int = 42) -> list[dict]:
    """Genera un lote reproducible de registros sintéticos para pruebas de volumen."""
    rng = random.Random(seed)
    records: list[dict] = []

    for i in range(1, count + 1):
        category = rng.choice(CATEGORIES)
        tags = rng.sample(TAG_POOL, k=rng.randint(2, 5))
        price = round(rng.uniform(25.0, 1200.0), 2)
        title = f"{category.capitalize()} {tags[0].upper()} Modelo-{i}"

        records.append({
            "id": i,
            "titulo": title,
            "categoria": category,
            "precio": price,
            "etiquetas": tags,
        })

    return records


def run_benchmark(num_records: int = 20000, top_k: int = 5) -> dict:
    """Mide los tiempos de indexación y búsqueda Top-K sobre un conjunto de datos."""
    records = generate_sample_records(count=num_records)

    index = SearchIndex()
    t0 = time.perf_counter()
    indexed_count = index.bulk_index(records)
    index_time_ms = (time.perf_counter() - t0) * 1000

    t1 = time.perf_counter()
    matches = search_and_rank(
        index=index,
        terms=["ssd", "nvme", "1tb"],
        top_k=top_k,
        match_all=False,
        max_price=300.0,
    )
    query_time_ms = (time.perf_counter() - t1) * 1000

    return {
        "registros_indexados": indexed_count,
        "tiempo_indexacion_ms": round(index_time_ms, 2),
        "tiempo_consulta_ms": round(query_time_ms, 2),
        "resultados_top_k": matches,
    }