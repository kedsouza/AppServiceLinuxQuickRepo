var location = resourceGroup().location

param id string
param user string
param appservicename string



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



