import datetime
import logging
import os

import azure.functions as func

from shared.pipedrive_client import PipedriveClient
from shared.sql_repository import SqlRepository
from shared.state_store import StateStore

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.timer_trigger(schedule="%TIMER_SCHEDULE%", arg_name="timer", run_on_startup=False, use_monitor=True)
def pipedrive_deal_ingestion(timer: func.TimerRequest) -> None:
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    logging.info("Iniciando sincronización de deals. UTC now=%s", utc_now.isoformat())

    lookback_minutes = int(os.getenv("SYNC_LOOKBACK_MINUTES", "30"))
    state_store = StateStore()
    repository = SqlRepository.from_key_vault()
    client = PipedriveClient.from_key_vault()

    last_update_time = state_store.get_last_update_time(repository)
    if not last_update_time:
        last_update_time = utc_now - datetime.timedelta(minutes=lookback_minutes)

    logging.info("Extrayendo deals actualizados desde %s", last_update_time.isoformat())
    deals = client.get_updated_deals(last_update_time)

    if not deals:
        logging.info("Sin cambios para persistir")
        return

    repository.upsert_deals(deals)
    max_update_time = max(
        datetime.datetime.fromisoformat(d["update_time"].replace("Z", "+00:00"))
        for d in deals
        if d.get("update_time")
    )
    state_store.set_last_update_time(repository, max_update_time)

    logging.info("Sincronización completada. Deals procesados=%s", len(deals))
