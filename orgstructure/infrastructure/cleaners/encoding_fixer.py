"""Correction du mojibake (UTF-8 mal décodé en Latin-1)."""

from typing import List, Optional
from dataclasses import replace

from orgstructure.domain.models import User, OrgNode


def _fix_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    try:
        return value.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return value


def _fix_user(user: User) -> User:
    return replace(
        user,
        display_name=_fix_text(user.display_name),
        mail=_fix_text(user.mail),
        user_principal_name=_fix_text(user.user_principal_name),
        department=_fix_text(user.department),
        job_title=_fix_text(user.job_title),
    )


def fix_encoding(nodes: List[OrgNode]) -> List[OrgNode]:
    """Corrige le mojibake sur tous les champs texte de chaque nœud."""
    return [
        replace(node, user=_fix_user(node.user),
                manager_display_name=_fix_text(node.manager_display_name))
        for node in nodes
    ]
