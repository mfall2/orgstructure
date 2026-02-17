"""Interface en ligne de commande."""

import argparse


def parse_args() -> argparse.Namespace:
    """Parse les arguments CLI : manager_name (positional) et --output."""
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
    return parser.parse_args()
