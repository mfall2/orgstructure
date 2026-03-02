"""Interface en ligne de commande."""

import argparse


def parse_args() -> argparse.Namespace:
    """Parse les arguments CLI : manager_name, --output et --mappings."""
    parser = argparse.ArgumentParser(
        description="Exporte la hiérarchie d'un manager Entra ID en CSV.",
    )
    parser.add_argument(
        "manager_name",
        help="Nom complet (displayName) du manager racine.",
    )
    parser.add_argument(
        "--output", default="direct_reports.csv",
        help="Fichier CSV de sortie (défaut : direct_reports.csv).",
    )
    parser.add_argument(
        "--mappings", default="title_mappings.json",
        help="Fichier JSON des règles de normalisation des titres (défaut : title_mappings.json).",
    )
    return parser.parse_args()
