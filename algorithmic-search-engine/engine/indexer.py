import re
from collections import defaultdict
from typing import Iterable, Optional


def normalize_token(text: str) -> str:
    """Limpia y normaliza texto o etiquetas a minúsculas sin espacios extra."""
    return re.sub(r"\s+", " ", text.strip().lower())


class SearchIndex:
    """Índice en memoria con soporte para búsqueda por etiquetas, texto y filtros."""

    def __init__(self) -> None:
        self.records: dict[int, dict] = {}
        self.tag_index: dict[str, set[int]] = defaultdict(set)
        self.category_index: dict[str, set[int]] = defaultdict(set)

    def add_record(self, record: dict) -> None:
        """Agrega un registro y actualiza los índices de categoría, etiquetas y título."""
        record_id = int(record["id"])
        self.records[record_id] = record

        category = normalize_token(str(record.get("categoria", "")))
        if category:
            self.category_index[category].add(record_id)

        for tag in record.get("etiquetas", []):
            norm_tag = normalize_token(str(tag))
            if norm_tag:
                self.tag_index[norm_tag].add(record_id)

        title = str(record.get("titulo", ""))
        for word in re.findall(r"[a-z0-9áéíóúñ]+", title.lower()):
            if len(word) >= 2:
                self.tag_index[word].add(record_id)

    def bulk_index(self, records: Iterable[dict]) -> int:
        """Indexa múltiples registros y devuelve cuántos se procesaron."""
        count = 0
        for rec in records:
            self.add_record(rec)
            count += 1
        return count

    def get_candidate_ids(self, terms: Iterable[str], match_all: bool = False) -> set[int]:
        """
        Devuelve IDs candidatos usando intersección (match_all=True)
        o unión (match_all=False) de conjuntos.
        """
        normalized_terms = [normalize_token(t) for t in terms if normalize_token(t)]
        if not normalized_terms:
            return set(self.records.keys())

        sets_list = [self.tag_index.get(term, set()) for term in normalized_terms]
        if not sets_list:
            return set()

        if match_all:
            return set.intersection(*sets_list)
        return set.union(*sets_list)

    def filter_by_price(
        self,
        candidate_ids: set[int],
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> set[int]:
        """Filtra un conjunto de IDs por rango de precio."""
        result: set[int] = set()
        for rid in candidate_ids:
            price = self.records[rid].get("precio")
            if price is None:
                continue
            if min_price is not None and price < min_price:
                continue
            if max_price is not None and price > max_price:
                continue
            result.add(rid)
        return result