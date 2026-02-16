targetScope = 'subscription'

@description('Nombre del resource group para la solución')
param resourceGroupName string = 'rg-mas-commercial-cockpit'

@description('Región Azure')
param location string = 'eastus2'

@description('Nombre lógico de la app')
param appName string = 'mas-commercial-cockpit'

@description('Usuario admin de SQL')
param sqlAdminLogin string

@secure()
@description('Password admin de SQL')
param sqlAdminPassword string

resource rg 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: resourceGroupName
  location: location
}

module infra './main.bicep' = {
  name: 'core-infra'
  scope: rg
  params: {
    location: location
    appName: appName
    sqlAdminLogin: sqlAdminLogin
    sqlAdminPassword: sqlAdminPassword
  }
}

output resourceGroupId string = rg.id
output sqlServerName string = infra.outputs.sqlServerName
output functionAppName string = infra.outputs.functionAppName
output keyVaultName string = infra.outputs.keyVaultName
