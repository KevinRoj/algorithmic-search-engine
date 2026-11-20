import heapq
from typing import Iterable, Optional
from .indexer import SearchIndex, normalize_token


def score_record(record: dict, query_terms: list[str]) -> int:
    """Calcula un puntaje de relevancia basado en coincidencias en etiquetas y título."""
    if not query_terms:
        return 1

    norm_tags = {normalize_token(str(t)) for t in record.get("etiquetas", [])}
    title_lower = str(record.get("titulo", "")).lower()

    score = 0
    for term in query_terms:
        if term in norm_tags:
            score += 3  # Mayor peso si coincide exactamente con una etiqueta
        if term in title_lower:
            score += 1  # Peso adicional si aparece en el título
    return score


def search_and_rank(
    index: SearchIndex,
    terms: Iterable[str],
    top_k: int = 5,
    match_all: bool = False,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
) -> list[dict]:
    """Busca, filtra y devuelve los Top-K registros ordenados por relevancia y precio."""
    if top_k <= 0:
        return []

    query_terms = [normalize_token(t) for t in terms if normalize_token(t)]
    candidate_ids = index.get_candidate_ids(query_terms, match_all=match_all)

    if category:
        norm_cat = normalize_token(category)
        cat_ids = index.category_index.get(norm_cat, set())
        candidate_ids = candidate_ids & cat_ids

    if min_price is not None or max_price is not None:
        candidate_ids = index.filter_by_price(
            candidate_ids,
            min_price=min_price,
            max_price=max_price,
        )

    scored_items: list[tuple[int, float, int, dict]] = []
    for rid in candidate_ids:
        rec = index.records[rid]
        pts = score_record(rec, query_terms)
        price = float(rec.get("precio", 0.0))
        # Mayor puntaje primero; ante empate, menor precio; luego menor ID para determinismo
        scored_items.append((pts, -price, -rid, rec))

    top_entries = heapq.nlargest(
        top_k,
        scored_items,
        key=lambda item: (item[0], item[1], item[2]),
    )

    results: list[dict] = []
    for pts, _, _, rec in top_entries:
        item_copy = dict(rec)
        item_copy["puntaje"] = pts
        results.append(item_copy)

    return results