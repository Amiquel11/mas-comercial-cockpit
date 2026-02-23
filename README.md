# mas-comercial-cockpit

## SQL connectivity in Azure Functions (Linux Flex Consumption)

This project uses `pymssql` for Azure SQL connectivity in Linux Flex Consumption, avoiding
an ODBC driver dependency (`pyodbc`) that is not available by default in that environment.
# mas-commercial-cockpit

Base inicial del repositorio para ingesta comercial desde Pipedrive, persistencia en Azure SQL y consumo en Power BI.

## Estructura
- `infra/`: despliegue Bicep de recursos Azure
- `src/ingestion/`: Azure Function (Python) con timer trigger
- `sql/`: modelo base, índices y vista para BI
- `powerbi/`: guía de modelo y medidas DAX

## Configuración local
### Prerrequisitos
- Python 3.11+
- Azure Functions Core Tools
- ODBC Driver 18 for SQL Server
- Azure CLI

### Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r src/ingestion/requirements.txt
cp src/ingestion/local.settings.example.json src/ingestion/local.settings.json
```

## Variables de entorno (Function)
Definir en `local.settings.json` o en App Settings:
- `KEY_VAULT_URL`
- `PIPEDRIVE_BASE_URL`
- `PIPEDRIVE_TOKEN_SECRET_NAME`
- `SQL_CONNECTION_SECRET_NAME`
- `SYNC_LOOKBACK_MINUTES`
- `TIMER_SCHEDULE`

## Deploy a Azure
1. Ajustar `infra/parameters.example.json` (o copiar a `parameters.dev.json`).
2. Ejecutar despliegue con Azure CLI:
```bash
az deployment sub create \
  --name mas-commercial-cockpit-bootstrap \
  --location eastus2 \
  --template-file infra/deploy-subscription.bicep \
  --parameters @infra/parameters.dev.json
```
3. Publicar la Function:
```bash
cd src/ingestion
func azure functionapp publish <function-app-name>
```
4. Ejecutar scripts SQL (`sql/001`, `sql/002`, `sql/003`) en la base creada.

## Cargar metas Excel desde Blob
Flujo recomendado:
1. Crear contenedor `targets` en la cuenta de Storage.
2. Subir archivo Excel con columnas mínimas: `Periodo`, `MetaCierresUF`, `MetaPipelineUF`, `MetaTicket`.
3. Consumir archivo desde Power BI con conector Azure Blob Storage.
4. Transformar en Power Query (tipos + validaciones) y relacionar con `Calendario`.

## Secretos requeridos en Key Vault
- `pipedrive-token`
- `sql-connection-string`
