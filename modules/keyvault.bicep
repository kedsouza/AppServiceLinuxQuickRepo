var location = resourceGroup().location

param id string
param user string
param appservicename string

resource appservice 'Microsoft.Web/sites@2024-04-01' existing ={
  name : appservicename
}

resource symbolicname 'Microsoft.Web/sites/config@2024-04-01' = {
  parent: appservice
  name: 'appsettings'
  properties: { keyvaultsecret :'@Microsoft.KeyVault(SecretUri=https://${kevyault.name}.vault.azure.net/secrets/kevaultsecret)'}
}

  

resource kevyault 'Microsoft.KeyVault/vaults@2024-11-01' = {
  name: '${user}-kv-${id}'
  location: location
  properties: {
    sku: {
      name: 'standard'
      family: 'A'
    }
    tenantId: tenant().tenantId
    accessPolicies: [
      
    ]
    enableRbacAuthorization: true
  }
}

resource secret 'Microsoft.KeyVault/vaults/secrets@2024-11-01' = {
  name: 'kevaultsecret'
  parent: kevyault 
  properties: {
    value: '123456789'
  }
}

var keyvaultRoleId = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
var keyvaultRoleAssignment = guid(resourceGroup().id, keyvaultRoleId)

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: keyvaultRoleAssignment
  properties: {
    principalId: appservice.identity.principalId
    roleDefinitionId: keyvaultRoleId
  }
}


