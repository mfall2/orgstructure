"""Ports (interfaces abstraites) d'accès aux données."""

from abc import ABC, abstractmethod
from typing import List
from .models import User


class UserRepository(ABC):
    """Contrat d'accès aux utilisateurs de l'annuaire."""

    @abstractmethod
    def find_by_name(self, name: str) -> User:
        """Recherche un utilisateur par displayName.

        Raises: UserNotFoundError, ExternalServiceError.
        """

    @abstractmethod
    def get_direct_reports(self, user_id: str) -> List[User]:
        """Retourne les subordonnés directs d'un utilisateur.

        Raises: ExternalServiceError.
        """
