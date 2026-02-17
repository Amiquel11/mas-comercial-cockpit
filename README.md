# mas-comercial-cockpit

## SQL connectivity in Azure Functions (Linux Flex Consumption)

This project uses `pymssql` for Azure SQL connectivity in Linux Flex Consumption, avoiding
an ODBC driver dependency (`pyodbc`) that is not available by default in that environment.
