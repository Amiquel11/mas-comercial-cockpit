import datetime
import os
from typing import Any

import requests

from .keyvault import get_secret


class PipedriveClient:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token

    @classmethod
    def from_key_vault(cls) -> "PipedriveClient":
        secret_name = os.getenv("PIPEDRIVE_TOKEN_SECRET_NAME", "pipedrive-token")
        token = get_secret(secret_name)
        base_url = os.getenv("PIPEDRIVE_BASE_URL", "https://api.pipedrive.com/v1")
        return cls(base_url=base_url, token=token)

    def get_updated_deals(self, since: datetime.datetime) -> list[dict[str, Any]]:
        endpoint = f"{self.base_url}/deals/collection"
        params = {
            "api_token": self.token,
            "limit": 500,
            "sort": "update_time ASC",
            "start": 0,
            "updated_since": since.strftime("%Y-%m-%d %H:%M:%S"),
        }

        all_rows: list[dict[str, Any]] = []
        while True:
            response = requests.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            payload = response.json()
            rows = payload.get("data") or []
            all_rows.extend(rows)

            additional = (payload.get("additional_data") or {}).get("pagination") or {}
            if not additional.get("more_items_in_collection"):
                break
            params["start"] = additional.get("next_start", params["start"] + params["limit"])

        return all_rows
