"""Cleaner composite : orchestre la correction d'encodage puis la normalisation."""

from pathlib import Path
from typing import List

from orgstructure.domain.models import OrgNode
from orgstructure.domain.ports import HierarchyCleaner
from .encoding_fixer import fix_encoding
from .title_normalizer import normalize_titles


class CompositeCleaner(HierarchyCleaner):
    """Applique séquentiellement la correction d'encodage et la normalisation des titres."""

    def __init__(self, mappings_path: Path) -> None:
        self._mappings_path = mappings_path

    def clean(self, nodes: List[OrgNode]) -> List[OrgNode]:
        nodes = fix_encoding(nodes)
        nodes = normalize_titles(nodes, self._mappings_path)
        return nodes
