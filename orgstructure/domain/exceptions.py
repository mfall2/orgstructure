"""Exceptions métier."""


class UserNotFoundError(Exception):
    """Utilisateur introuvable dans l'annuaire."""


class ExternalServiceError(Exception):
    """Erreur de communication avec un service externe (Graph API, Azure CLI)."""
