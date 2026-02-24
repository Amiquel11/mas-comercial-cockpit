# mas-comercial-cockpit

## SQL connectivity in Azure Functions (Linux Flex Consumption)

This project uses `pymssql` for Azure SQL connectivity in Linux Flex Consumption, avoiding
an ODBC driver dependency (`pyodbc`) that is not available by default in that environment.

## Deployment structure (important)

The Azure Function App source lives under `src/ingestion`.
The GitHub Actions workflow deploys **that folder** as the package root.

For successful deployment and function discovery:
- `src/ingestion/host.json` must exist.
- `src/ingestion/function_app.py` must exist.
- `src/ingestion/requirements.txt` should contain runtime dependencies.

## GitHub Actions deployment note

The workflow deploys using `publish-profile` (`AZURE_FUNCTIONAPP_PUBLISH_PROFILE`) instead of
`azure/login` with subscription-based auth.


Authentication in CI supports either publish profile secrets (`AZURE_FUNCTIONAPP_PUBLISH_PROFILE` or `AZUREAPPSERVICE_PUBLISHPROFILE`) or RBAC via `AZURE_CREDENTIALS` with `azure/login`.

Also verify Function App settings in Azure:
- `FUNCTIONS_WORKER_RUNTIME=python`
- `AzureWebJobsStorage` configured
If these are missing, deployment can succeed but no functions will be indexed in the portal.
