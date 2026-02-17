"""Point d'entrée — usage : python main.py "Nom Du Manager" --output resultats.csv"""

import sys

from orgstructure.infrastructure.graph.repository import GraphUserRepository
from orgstructure.domain.services import OrganizationService
from orgstructure.domain.exceptions import UserNotFoundError, ExternalServiceError
from orgstructure.infrastructure.exporters.csv_exporter import CsvExporter
from orgstructure.interfaces.cli import parse_args


def main() -> None:
    args = parse_args()

    try:
        repository = GraphUserRepository()
        service = OrganizationService(repository)
        hierarchy = service.get_full_hierarchy(args.manager_name)
    except UserNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except ExternalServiceError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    try:
        CsvExporter.export(hierarchy, args.output)
    except (FileNotFoundError, PermissionError) as exc:
        print(f"Error writing output file: {exc}", file=sys.stderr)
        sys.exit(3)

    print(f"Exported {len(hierarchy)} users to {args.output}")


if __name__ == "__main__":
    main()
