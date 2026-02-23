import datetime
import json
import os
from typing import Any

import pyodbc

from .keyvault import get_secret


class SqlRepository:
    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string

    @classmethod
    def from_key_vault(cls) -> "SqlRepository":
        secret_name = os.getenv("SQL_CONNECTION_SECRET_NAME", "sql-connection-string")
        connection_string = get_secret(secret_name)
        return cls(connection_string)

    def _connect(self) -> pyodbc.Connection:
        return pyodbc.connect(self.connection_string)

    def get_watermark(self, process_name: str) -> datetime.datetime | None:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT last_update_time FROM dbo.etl_watermark WHERE process_name = ?",
                process_name,
            )
            row = cursor.fetchone()
            return row[0] if row else None

    def set_watermark(self, process_name: str, value: datetime.datetime) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                MERGE dbo.etl_watermark AS t
                USING (SELECT ? AS process_name, ? AS last_update_time) AS s
                ON t.process_name = s.process_name
                WHEN MATCHED THEN
                  UPDATE SET last_update_time = s.last_update_time, updated_at = SYSUTCDATETIME()
                WHEN NOT MATCHED THEN
                  INSERT (process_name, last_update_time, updated_at)
                  VALUES (s.process_name, s.last_update_time, SYSUTCDATETIME());
                """,
                process_name,
                value,
            )
            conn.commit()

    def upsert_deals(self, deals: list[dict[str, Any]]) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            for deal in deals:
                user = deal.get("user_id") or {}
                org = deal.get("org_id") or {}

                cursor.execute(
                    """
                    MERGE dbo.dim_user AS t
                    USING (SELECT ? AS user_id, ? AS user_name) AS s
                    ON t.user_id = s.user_id
                    WHEN MATCHED THEN UPDATE SET user_name = s.user_name, updated_at = SYSUTCDATETIME()
                    WHEN NOT MATCHED THEN INSERT (user_id, user_name, updated_at)
                    VALUES (s.user_id, s.user_name, SYSUTCDATETIME());
                    """,
                    _extract_value(user),
                    _extract_label(user),
                )

                cursor.execute(
                    """
                    MERGE dbo.dim_org AS t
                    USING (SELECT ? AS org_id, ? AS org_name) AS s
                    ON t.org_id = s.org_id
                    WHEN MATCHED THEN UPDATE SET org_name = s.org_name, updated_at = SYSUTCDATETIME()
                    WHEN NOT MATCHED THEN INSERT (org_id, org_name, updated_at)
                    VALUES (s.org_id, s.org_name, SYSUTCDATETIME());
                    """,
                    _extract_value(org),
                    _extract_label(org),
                )

                cursor.execute(
                    """
                    MERGE dbo.fact_deal_current AS t
                    USING (SELECT ? AS deal_id) AS s
                    ON t.deal_id = s.deal_id
                    WHEN MATCHED THEN UPDATE SET
                      title = ?, value = ?, currency = ?, status = ?, stage_id = ?,
                      user_id = ?, org_id = ?, update_time = ?, raw_payload = ?, updated_at = SYSUTCDATETIME()
                    WHEN NOT MATCHED THEN
                      INSERT (deal_id, title, value, currency, status, stage_id, user_id, org_id, update_time, raw_payload, updated_at)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, SYSUTCDATETIME());
                    """,
                    deal.get("id"),
                    deal.get("title"), deal.get("value"), deal.get("currency"), deal.get("status"), deal.get("stage_id"),
                    _extract_value(user), _extract_value(org), deal.get("update_time"), json.dumps(deal),
                    deal.get("id"), deal.get("title"), deal.get("value"), deal.get("currency"), deal.get("status"), deal.get("stage_id"),
                    _extract_value(user), _extract_value(org), deal.get("update_time"), json.dumps(deal),
                )

                cursor.execute(
                    """
                    INSERT INTO dbo.fact_deal_stage_event (
                      deal_id, stage_id, status, event_update_time, value, currency, captured_at
                    ) VALUES (?, ?, ?, ?, ?, ?, SYSUTCDATETIME())
                    """,
                    deal.get("id"), deal.get("stage_id"), deal.get("status"), deal.get("update_time"), deal.get("value"), deal.get("currency")
                )

            conn.commit()


def _extract_value(field: Any) -> Any:
    if isinstance(field, dict):
        return field.get("value")
    return field


def _extract_label(field: Any) -> str | None:
    if isinstance(field, dict):
        return field.get("name") or field.get("label")
    return None
