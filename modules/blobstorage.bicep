var location = resourceGroup().location

param name string

resource blobstorage 'Microsoft.Storage/storageAccounts@2024-01-01' = {
  name: name
  location: location
  sku: {
    name: 'Standard_LRS'	
  }
  kind: 'BlobStorage'
  properties: {
    accessTier: 'Cold'
  }
}
