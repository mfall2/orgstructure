"""Export des nœuds organisationnels au format CSV."""

import csv
from typing import List
from orgstructure.domain.models import OrgNode

_CSV_COLUMNS = [
    "level", "managerName", "displayName",
    "mail", "userPrincipalName", "department", "jobTitle",
]


class CsvExporter:
    """Exporte une liste d'OrgNode en CSV (UTF-8)."""

    @staticmethod
    def export(nodes: List[OrgNode], filename: str) -> None:
        """Écrit les nœuds dans un fichier CSV avec liens hiérarchiques."""
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(_CSV_COLUMNS)

            for node in nodes:
                writer.writerow([
                    node.level,
                    node.manager_display_name or "",
                    node.user.display_name,
                    node.user.mail,
                    node.user.user_principal_name,
                    node.user.department,
                    node.user.job_title,
                ])
