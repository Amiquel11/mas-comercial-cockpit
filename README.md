# mas-comercial-cockpit

## SQL connectivity in Azure Functions (Linux Flex Consumption)

This project uses `pymssql` for Azure SQL connectivity in Linux Flex Consumption, avoiding
an ODBC driver dependency (`pyodbc`) that is not available by default in that environment.

## GitHub Actions deployment note

The workflow deploys using `publish-profile` (`AZURE_FUNCTIONAPP_PUBLISH_PROFILE`) instead of
`azure/login` with subscription-based auth. This avoids common CI failures such as:
- `No subscriptions found for ***`
- `Double check if the 'auth-type' is correct`

If deployment fails, regenerate the Function App publish profile in Azure Portal and update the
repository secret.
