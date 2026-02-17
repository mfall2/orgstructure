# EntraOrgExplorer

Explore la hiérarchie organisationnelle d'un tenant Microsoft Entra ID via l'API Microsoft Graph.
À partir d'un manager, parcourt récursivement tous les subordonnés et exporte le résultat en CSV.

## Prérequis

- Python 3.9+
- [Azure CLI](https://aka.ms/installazurecli) connecté (`az login`)
- Permissions Entra ID : `User.Read.All` ou `Directory.Read.All`

## Installation

```bash
pip install -r requirements.txt
az login
```

## Utilisation

```bash
python main.py "Eric Terreau" --output resultats.csv
```

| Argument       | Obligatoire | Description                        | Défaut              |
|----------------|:-----------:|------------------------------------|---------------------|
| `manager_name` | oui         | displayName du manager racine      | —                   |
| `--output`     | non         | Fichier CSV de sortie              | `direct_reports.csv` |

## Colonnes CSV

| Colonne             | Description                                                |
|---------------------|------------------------------------------------------------|
| `level`             | Niveau hiérarchique (0 = racine, 1 = N-1, 2 = N-2, etc.) |
| `managerName`       | Nom du manager direct (vide pour la racine)                |
| `displayName`       | Nom complet                                                |
| `mail`              | Adresse e-mail                                             |
| `userPrincipalName` | Identifiant UPN                                            |
| `department`        | Département                                                |
| `jobTitle`          | Intitulé du poste                                          |

## Architecture

Clean Architecture (hexagonale) :

```
main.py                          # Point d'entrée
orgstructure/
├── domain/
│   ├── models.py                # User, OrgNode
│   ├── ports.py                 # Interface UserRepository
│   ├── services.py              # Parcours BFS de la hiérarchie
│   └── exceptions.py            # UserNotFoundError, ExternalServiceError
├── infrastructure/
│   ├── graph/
│   │   ├── auth.py              # Token via Azure CLI (cache 5 min)
│   │   └── repository.py        # Graph API (retry, pagination, OData)
│   └── exporters/
│       └── csv_exporter.py      # Export CSV
└── interfaces/
    └── cli.py                   # Parsing des arguments
```

## Codes de sortie

| Code | Signification                              |
|:----:|--------------------------------------------|
| `0`  | Succès                                     |
| `1`  | Utilisateur non trouvé                     |
| `2`  | Erreur Microsoft Graph / Azure CLI         |
| `3`  | Erreur écriture fichier                    |
