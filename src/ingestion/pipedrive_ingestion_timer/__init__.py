import logging

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    if mytimer.past_due:
        logging.warning("Pipedrive ingestion timer is running late.")

    logging.info("Pipedrive ingestion timer triggered (every 5 minutes).")
