var location = resourceGroup().location

param appservicename string

param id string
param user string
param bothstoragetypes int


resource storage 'Microsoft.Storage/storageAccounts@2024-01-01' = {
  name: '${user}storage${id}'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}

resource filestorage 'Microsoft.Storage/storageAccounts/fileServices@2024-01-01' = {
  name: 'default'
  parent: storage
}


resource share 'Microsoft.Storage/storageAccounts/fileServices/shares@2024-01-01' = {
  name: 'testfileshare'
  parent: filestorage
}

resource appservice 'Microsoft.Web/sites@2024-04-01'existing = {
  name: appservicename
}

// // Check if blob storage exits.
// resource blobServices 'Microsoft.Storage/storageAccounts/blobServices@2024-01-01'existing = {
//   parent: storage
//   name: 'default'
// }

// resource containers 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' existing =  {
//   parent: blobServices
//   name: 'testblob'
// }

// var blobname = containers.name

var fileproperties ={
  'files ': {
   type :'AzureFiles'
   shareName: share.name
   mountPath: '/storagefile'
   accountName: storage.name
   accessKey: storage.listKeys().keys[0].value
 }
}

var blobproperties = {
'blob ': {
        type: 'AzureBlob'
        shareName: 'testblob'
        mountPath: '/storageblob'
        accountName: storage.name
        accessKey: storage.listKeys().keys[0].value
    }
}

var storageproperties =  (bothstoragetypes == 1) ?union(fileproperties, blobproperties) : fileproperties

//var mgmtStatus = ((empty(blobname)) ?   fileproperties : union(fileproperties, blobproperties))

resource storagemount 'Microsoft.Web/sites/config@2024-04-01' = {
  name: 'azurestorageaccounts'
  parent: appservice
  properties: storageproperties
  dependsOn: [
    storage
  ]
}



