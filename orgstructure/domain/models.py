"""Entités du domaine."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class User:
    """Utilisateur Entra ID."""

    id: str
    display_name: str
    mail: Optional[str]
    user_principal_name: Optional[str]
    department: Optional[str]
    job_title: Optional[str]


@dataclass(frozen=True)
class OrgNode:
    """Nœud hiérarchique : un utilisateur relié à son manager direct."""

    user: User
    level: int
    manager_id: Optional[str] = None
    manager_display_name: Optional[str] = None
