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

resource blobServices 'Microsoft.Storage/storageAccounts/blobServices@2024-01-01'  = {
  parent: storage
  name: 'default'
}

resource containers 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' =  {
  parent: blobServices
  name: 'testblob'
}

resource appservice 'Microsoft.Web/sites@2024-04-01'existing = {
  name: appservicename
}

// // Check if file storage exists.
// resource filestorage 'Microsoft.Storage/storageAccounts/fileServices@2024-01-01'existing = {
//   name: 'default'
//   parent: storage
// }


// resource share 'Microsoft.Storage/storageAccounts/fileServices/shares@2024-01-01' existing = {
//   name: 'testfileshare'
//   parent: filestorage
// }

// var sharename = share.id


var fileproperties ={
    'files ': {
     type :'AzureFiles'
     shareName: 'testfileshare'
     mountPath: '/storagefile'
     accountName: storage.name
     accessKey: storage.listKeys().keys[0].value
   }
}

var blobproperties = {
'blob ': {
          type: 'AzureBlob'
          shareName: containers.name
          mountPath: '/storageblob'
          accountName: storage.name
          accessKey: storage.listKeys().keys[0].value
      }
}
var storageproperties =  (bothstoragetypes == 1) ?union(fileproperties, blobproperties) : blobproperties


//var mgmtStatus = ((empty(fileshareid)) ?  blobproperties : union(fileproperties, blobproperties))

resource storagemount 'Microsoft.Web/sites/config@2024-04-01' = {
  name: 'azurestorageaccounts'
  parent: appservice
  properties: storageproperties

  dependsOn: [
    storage
  ]
}

@description('The properties of the blobstorage')
output blobproperties object = storageproperties


