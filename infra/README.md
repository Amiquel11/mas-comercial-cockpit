# Infraestructura Azure (Bicep)

Este módulo despliega la base mínima en Azure:
- Resource Group
- Azure SQL Server + Database
- Function App (Python)
- Key Vault
- Application Insights

## Requisitos
- Azure CLI (`az`)
- Permisos para despliegue a nivel de suscripción

## Variables parametrizadas
Las variables se definen en `parameters.example.json`:
- `resourceGroupName`
- `location`
- `appName`
- `sqlAdminLogin`
- `sqlAdminPassword` (secure)

## Despliegue
1. Copia y ajusta parámetros:
```bash
cp infra/parameters.example.json infra/parameters.dev.json
```

2. Inicia sesión y selecciona suscripción:
```bash
az login
az account set --subscription "<subscription-id>"
```

3. Ejecuta despliegue a nivel suscripción:
```bash
az deployment sub create \
  --name mas-commercial-cockpit-bootstrap \
  --location eastus2 \
  --template-file infra/deploy-subscription.bicep \
  --parameters @infra/parameters.dev.json
```

## Post-despliegue
- Asigna a la identidad administrada de la Function App permisos `Key Vault Secrets User` sobre el Key Vault.
- Guarda secretos mínimos en Key Vault:
  - `pipedrive-token`
  - `sql-connection-string`
