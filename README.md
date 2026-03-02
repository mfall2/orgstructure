# EntraOrgExplorer



## Vue d'ensemble

C'est un outil en ligne de commande Python qui explore la hiérarchie organisationnelle d'un tenant Microsoft Entra ID (anciennement Azure AD) via l'API Microsoft Graph. À partir du nom d'un manager, il reconstruit toute l'arborescence de ses subordonnés (directs et indirects) et l'exporte en CSV.

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

Le projet suit une architecture hexagonale (Clean Architecture) avec trois couches bien séparées :
1. Domaine (orgstructure/domain/)
models.py — Deux dataclasses : User (identité d'un utilisateur Entra) et OrgNode (un noeud dans l'arbre hiérarchique, avec niveau et lien vers le manager).
ports.py — Le port UserRepository (interface abstraite ABC) qui définit deux opérations : find_by_name() et get_direct_reports().
services.py — OrganizationService qui contient la logique métier : un parcours en largeur (BFS) à partir d'un manager racine pour construire toute la hiérarchie.
exceptions.py — Exceptions métier : UserNotFoundError et ExternalServiceError.
2. Infrastructure (orgstructure/infrastructure/)
graph/auth.py — AzureCliAuth : obtient un token OAuth2 via la commande az account get-access-token (Azure CLI), avec un cache de 5 minutes.
graph/repository.py — GraphUserRepository : l'implémentation concrète du port UserRepository, qui appelle l'API Microsoft Graph v1.0. Gère la pagination (@odata.nextLink) et le retry avec backoff exponentiel sur les erreurs HTTP 429/5xx.
exporters/csv_exporter.py — CsvExporter : exporte la liste d'OrgNode en fichier CSV UTF-8 avec les colonnes : level, managerName, displayName, mail, userPrincipalName, department, jobTitle.
3. Interface (orgstructure/interfaces/)
cli.py — Parsing des arguments avec argparse : un argument positionnel manager_name et une option --output (défaut : direct_reports.csv).
Point d'entrée (main.py)
Orchestre le tout : parse les arguments, instancie le repository et le service, lance get_full_hierarchy(), exporte le CSV, et gère les codes de sortie (0 = succès, 1 = utilisateur non trouvé, 2 = erreur Graph/Azure CLI, 3 = erreur d'écriture fichier).

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

## Flux de données

- L'utilisateur lance python main.py "Nom du Manager" --output fichier.csv
- Le programme s'authentifie via Azure CLI (az login doit avoir été fait au préalable)
- Il cherche l'utilisateur par son displayName via un filtre OData sur Graph API
- Il parcourt en BFS tous les directReports récursivement
- Il construit une liste plate d'OrgNode ordonnée par niveau hiérarchique
- Il exporte le tout en CSV

## Codes de sortie

| Code | Signification                              |
|:----:|--------------------------------------------|
| `0`  | Succès                                     |
| `1`  | Utilisateur non trouvé                     |
| `2`  | Erreur Microsoft Graph / Azure CLI         |
| `3`  | Erreur écriture fichier                    |


## Dépendance unique

requests>=2.31.0 (pour les appels HTTP à Graph API)