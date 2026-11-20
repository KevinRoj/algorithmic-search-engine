import logging
from engine import SearchIndex, generate_sample_records, run_benchmark, search_and_rank

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

SAMPLE_CATALOG = [
    {
        "id": 1,
        "titulo": "SSD NVMe 1TB PCIe Gen4",
        "categoria": "almacenamiento",
        "precio": 78.00,
        "etiquetas": ["ssd", "nvme", "1tb", "gen4"],
    },
    {
        "id": 2,
        "titulo": "SSD NVMe 2TB Alta Velocidad",
        "categoria": "almacenamiento",
        "precio": 135.00,
        "etiquetas": ["ssd", "nvme", "2tb", "gen4"],
    },
    {
        "id": 3,
        "titulo": "Tarjeta Grafica RTX 4060 8GB",
        "categoria": "graficos",
        "precio": 310.00,
        "etiquetas": ["rtx", "gpu", "8gb", "nvidia"],
    },
    {
        "id": 4,
        "titulo": "Memoria RAM DDR5 32GB 6000MHz",
        "categoria": "memoria",
        "precio": 115.00,
        "etiquetas": ["ddr5", "32gb", "6000mhz", "ram"],
    },
    {
        "id": 5,
        "titulo": "Teclado Mecanico Inalambrico",
        "categoria": "perifericos",
        "precio": 64.50,
        "etiquetas": ["mecanico", "inalambrico", "teclado"],
    },
]


def main() -> None:
    index = SearchIndex()
    total = index.bulk_index(SAMPLE_CATALOG)
    logging.info(f"Catálogo base indexado: {total} registros.")

    results = search_and_rank(index=index, terms=["ssd", "nvme", "1tb"], top_k=3)
    logging.info("Resultados de búsqueda ['ssd', 'nvme', '1tb']:")
    for item in results:
        logging.info(
            f"  - #{item['id']} | {item['titulo']} | ${item['precio']:.2f} | puntaje={item['puntaje']}"
        )

    bench = run_benchmark(num_records=20000, top_k=5)
    logging.info(
        f"Benchmark ({bench['registros_indexados']} registros): "
        f"indexación={bench['tiempo_indexacion_ms']} ms | "
        f"consulta Top-K={bench['tiempo_consulta_ms']} ms"
    )

    logging.info("Top-K del benchmark (filtro ['ssd', 'nvme', '1tb'], max_price=300.0):")
    for item in bench["resultados_top_k"]:
        etiquetas_str = ", ".join(item["etiquetas"])
        logging.info(
            f"  - #{item['id']} | {item['titulo']} | {item['categoria']} | "
            f"${item['precio']:.2f} | puntaje={item['puntaje']} | tags=[{etiquetas_str}]"
        )

    sample_batch = generate_sample_records(count=5)
    logging.info("Muestra de los primeros 5 registros sintéticos generados:")
    for rec in sample_batch:
        logging.info(
            f"  - #{rec['id']} | {rec['titulo']} | {rec['categoria']} | "
            f"${rec['precio']:.2f} | tags={rec['etiquetas']}"
        )


if __name__ == "__main__":
    main()