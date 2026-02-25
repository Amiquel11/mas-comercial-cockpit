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


## Troubleshooting: deploy succeeds but no functions appear

If deployment is successful but the Functions list is empty in Azure Portal:
- Verify app settings: `FUNCTIONS_WORKER_RUNTIME=python`, `FUNCTIONS_EXTENSION_VERSION=~4`, and `AzureWebJobsStorage`.
- Check **Log stream** or Application Insights for indexing errors (e.g., `No job functions found`, import errors).
- Confirm `src/ingestion/host.json` includes an extension bundle for non-HTTP triggers (Timer uses extension bundle).
- Restart the Function App after deployment and wait 1-3 minutes for indexing.
