import logging
from dataclasses import dataclass
from typing import Any, Iterable, Optional

import pymssql

logger = logging.getLogger(__name__)


@dataclass
class SqlConnectionConfig:
    server: str
    port: int
    database: str
    user: str
    password: str


class SqlRepository:
    """
    Repository for Azure SQL access using pymssql (pure Python driver).

    Note: pymssql uses ``%s`` placeholders for query parameters.
    """

    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    @staticmethod
    def _parse_ado_connection_string(connection_string: str) -> SqlConnectionConfig:
        """
        Parse ADO.NET style connection strings, e.g.:
        "Server=tcp:<server>.database.windows.net,1433;Initial Catalog=<db>;User ID=<user>;Password=<pass>;Encrypt=True;..."
        """
        if not connection_string:
            raise ValueError("Connection string is empty")

        segments = [segment.strip() for segment in connection_string.split(";") if segment.strip()]
        raw_params: dict[str, str] = {}
        for segment in segments:
            if "=" not in segment:
                continue
            key, value = segment.split("=", 1)
            raw_params[key.strip().lower()] = value.strip()

        server_value = raw_params.get("server") or raw_params.get("data source")
        database = raw_params.get("initial catalog") or raw_params.get("database")
        user = raw_params.get("user id") or raw_params.get("uid")
        password = raw_params.get("password") or raw_params.get("pwd")

        if not server_value:
            raise ValueError("Missing Server in connection string")
        if not database:
            raise ValueError("Missing Initial Catalog/Database in connection string")
        if not user:
            raise ValueError("Missing User ID in connection string")
        if password is None:
            raise ValueError("Missing Password in connection string")

        server_value = server_value.removeprefix("tcp:")
        port = 1433
        if "," in server_value:
            host_part, port_part = server_value.rsplit(",", 1)
            server_value = host_part.strip()
            if port_part.strip():
                port = int(port_part.strip())

        return SqlConnectionConfig(
            server=server_value,
            port=port,
            database=database,
            user=user,
            password=password,
        )

    def _connect(self) -> pymssql.Connection:
        config = self._parse_ado_connection_string(self.connection_string)

        logger.info(
            "Opening SQL connection to server '%s' on port %s (database '%s').",
            config.server,
            config.port,
            config.database,
        )

        return pymssql.connect(
            server=config.server,
            user=config.user,
            password=config.password,
            database=config.database,
            port=config.port,
            login_timeout=30,
            timeout=30,
        )

    @staticmethod
    def _normalize_query_placeholders(query: str) -> str:
        """
        Compatibility helper: converts legacy pyodbc '?' placeholders to pymssql '%s'.
        If queries are already migrated to '%s', this leaves them unchanged.
        """
        return query.replace("?", "%s") if "?" in query else query

    def fetch_all(self, query: str, params: Optional[Iterable[Any]] = None) -> list[dict[str, Any]]:
        query = self._normalize_query_placeholders(query)
        with self._connect() as connection:
            with connection.cursor(as_dict=True) as cursor:
                cursor.execute(query, tuple(params or ()))
                return list(cursor.fetchall())

    def execute(self, query: str, params: Optional[Iterable[Any]] = None) -> int:
        query = self._normalize_query_placeholders(query)
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, tuple(params or ()))
                connection.commit()
                return cursor.rowcount

    def execute_many(self, query: str, params_list: Iterable[Iterable[Any]]) -> int:
        query = self._normalize_query_placeholders(query)
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.executemany(query, [tuple(params) for params in params_list])
                connection.commit()
                return cursor.rowcount
