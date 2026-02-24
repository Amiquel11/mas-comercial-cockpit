import datetime

from .sql_repository import SqlRepository


class StateStore:
    PROCESS_NAME = "pipedrive_deal_ingestion"

    def get_last_update_time(self, repository: SqlRepository) -> datetime.datetime | None:
        return repository.get_watermark(self.PROCESS_NAME)

    def set_last_update_time(self, repository: SqlRepository, value: datetime.datetime) -> None:
        repository.set_watermark(self.PROCESS_NAME, value)
