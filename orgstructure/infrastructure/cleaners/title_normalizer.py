"""Normalisation des intitulés de poste via un fichier de mappings externe."""

import json
import re
from pathlib import Path
from typing import List
from dataclasses import replace

from orgstructure.domain.models import User, OrgNode


def _load_mappings(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _normalize_title(title: str, mappings: list[dict]) -> str:
    for rule in mappings:
        if re.fullmatch(rule["pattern"], title):
            return rule["replacement"]
    return title


def normalize_titles(nodes: List[OrgNode], mappings_path: Path) -> List[OrgNode]:
    """Normalise le champ job_title de chaque nœud selon les règles de mappings."""
    mappings = _load_mappings(mappings_path)
    result = []
    for node in nodes:
        if node.user.job_title:
            new_title = _normalize_title(node.user.job_title, mappings)
            new_user = replace(node.user, job_title=new_title)
            result.append(replace(node, user=new_user))
        else:
            result.append(node)
    return result
