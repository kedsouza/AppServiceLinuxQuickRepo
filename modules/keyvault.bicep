var location = resourceGroup().location

param name string

param appservicename string



resource kevyault 'Microsoft.KeyVault/vaults@2024-11-01' = {
  name: 'k${name}'
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



