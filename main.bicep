var location = resourceGroup().location

resource appserviceplan 'Microsoft.Web/serverfarms@2024-04-01' = {
  name: 'asp-${uniqueString(resourceGroup().id)}'
  location: location
  kind: 'linux'
  sku: {
    name: 'B3'
  }
  properties: {
    reserved: true
  }
}

resource appservice 'Microsoft.Web/sites@2024-04-01' = {
  name: 'asp-${uniqueString(resourceGroup().id)}'
  location: location
  properties : {
    serverFarmId: appserviceplan.id
    siteConfig: {
      linuxFxVersion: 'node|16-lts'
      appSettings: [
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
      ]
    }
  }
}

var identity = '/subscriptions/bf7728b1-4728-478d-96bc-db17b8ebc9ff/resourceGroups/kedsouza-ca-vnet-v2/providers/Microsoft.ManagedIdentity/userAssignedIdentities/kedsouza-user-mi'

resource deploymentScript 'Microsoft.Resources/deploymentScripts@2023-08-01' = {
  name: 'inLine-Ci-${uniqueString(resourceGroup().id)}'
  location: location
  kind: 'AzureCLI'
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identity}': {}
    }
  }
  properties: {
    azCliVersion: '2.52.0'
    retentionInterval: 'PT1H'
    scriptContent: 'az webapp deploy --resource-group ${resourceGroup().name} --name ${appservice.name} --src-url https://raw.githubusercontent.com/kedsouza/test-bicep/refs/heads/main/app.zip --type zip'
    //scriptContent: 'az login --service-principal --username 9408fe2b-528c-40b0-baea-a9b56446eebb --password ctk8Q~T6N3wjhA4DF6-s_nOLLZLzVU9mUVfB0a7l --tenant 16b3c013-d300-468d-ac64-7eda0820b6d3; az webapp deploy --resource-group ${resourceGroup().name} --name ${appservice.name} --src-url https://kedsouzastorage1.file.core.windows.net/test/app.zip --type zip'

  }
}

