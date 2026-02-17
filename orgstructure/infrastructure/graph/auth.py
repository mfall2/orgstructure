"""Authentification Microsoft Graph via Azure CLI.

Obtient un token OAuth2 via `az account get-access-token` et le met en cache 5 min.
"""

import shutil
import subprocess
import time

from orgstructure.domain.exceptions import ExternalServiceError

_TOKEN_CACHE_SECONDS = 300


class AzureCliAuth:
    """Fournit un token Bearer pour Microsoft Graph via Azure CLI."""

    def __init__(self):
        self._token: str | None = None
        self._expires_at: float = 0

    def get_token(self) -> str:
        """Retourne un token valide (cache ou nouveau via `az`).

        Raises: ExternalServiceError si Azure CLI est absent ou en erreur.
        """
        if self._token and time.time() < self._expires_at:
            return self._token

        az_path = shutil.which("az")
        if az_path is None:
            raise ExternalServiceError(
                "Azure CLI ('az') not found. "
                "Install it from https://aka.ms/installazurecli and run 'az login'."
            )

        try:
            result = subprocess.run(
                [az_path, "account", "get-access-token",
                 "--resource", "https://graph.microsoft.com/",
                 "--query", "accessToken", "-o", "tsv"],
                capture_output=True, text=True, check=True,
            )
        except subprocess.CalledProcessError as exc:
            stderr = exc.stderr.strip() if exc.stderr else "unknown error"
            raise ExternalServiceError(
                f"Azure CLI failed (exit {exc.returncode}): {stderr}"
            ) from exc

        token = result.stdout.strip()
        if not token:
            raise ExternalServiceError(
                "Azure CLI returned an empty token. Run 'az login' and try again."
            )

        self._token = token
        self._expires_at = time.time() + _TOKEN_CACHE_SECONDS
        return self._token
