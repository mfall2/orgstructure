"""Implémentation UserRepository via l'API Microsoft Graph v1.0."""

import requests
import time
from typing import List
from urllib.parse import quote

from orgstructure.domain.models import User
from orgstructure.domain.ports import UserRepository
from orgstructure.domain.exceptions import UserNotFoundError, ExternalServiceError
from .auth import AzureCliAuth

_USER_FIELDS = "id,displayName,mail,userPrincipalName,department,jobTitle"
_RETRYABLE_STATUS_CODES = (429, 500, 502, 503)


class GraphUserRepository(UserRepository):
    """Accès aux utilisateurs Entra ID via Microsoft Graph.

    Inclut : retry avec backoff exponentiel et pagination automatique.
    """

    BASE_URL = "https://graph.microsoft.com/v1.0"

    def __init__(self):
        self.auth = AzureCliAuth()

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.auth.get_token()}",
            "Accept": "application/json",
        }

    def _get_with_retry(self, url: str, max_attempts: int = 5) -> dict:
        """GET avec retry (backoff exponentiel) sur erreurs 429/5xx."""
        for attempt in range(1, max_attempts + 1):
            response = requests.get(url, headers=self._headers())

            if 200 <= response.status_code < 300:
                return response.json()

            if response.status_code in _RETRYABLE_STATUS_CODES:
                time.sleep(2 ** attempt)
                continue

            raise ExternalServiceError(response.text)

        raise ExternalServiceError("Max retries exceeded")

    def find_by_name(self, name: str) -> User:
        """Recherche un utilisateur par displayName (filtre OData encodé)."""
        escaped = name.replace("'", "''")
        encoded_filter = quote(f"displayName eq '{escaped}'", safe="")
        url = (
            f"{self.BASE_URL}/users?"
            f"$filter={encoded_filter}&$select={_USER_FIELDS}"
        )

        data = self._get_with_retry(url)
        if not data.get("value"):
            raise UserNotFoundError(f"User '{name}' not found")

        return self._to_user(data["value"][0])

    def get_direct_reports(self, user_id: str) -> List[User]:
        """Retourne les subordonnés directs (avec pagination @odata.nextLink)."""
        url = f"{self.BASE_URL}/users/{user_id}/directReports?$select={_USER_FIELDS}"
        users = []

        while url:
            data = self._get_with_retry(url)
            users.extend(self._to_user(item) for item in data.get("value", []))
            url = data.get("@odata.nextLink")

        return users

    @staticmethod
    def _to_user(item: dict) -> User:
        return User(
            id=item["id"],
            display_name=item.get("displayName"),
            mail=item.get("mail"),
            user_principal_name=item.get("userPrincipalName"),
            department=item.get("department"),
            job_title=item.get("jobTitle"),
        )
