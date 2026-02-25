import logging

import azure.functions as func

app = func.FunctionApp()


@app.function_name(name="health")
@app.route(route="health", auth_level=func.AuthLevel.FUNCTION)
def health(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("ok", status_code=200)


@app.function_name(name="pipedrive_ingestion_timer")
@app.schedule(schedule="0 */5 * * * *", arg_name="timer", run_on_startup=False, use_monitor=True)
def pipedrive_ingestion_timer(timer: func.TimerRequest) -> None:
    if timer.past_due:
        logging.warning("Pipedrive ingestion timer is running late.")

    logging.info("Pipedrive ingestion timer triggered (every 5 minutes).")
