param(
    [string]$AccountName,
    [ValidateSet('Standard_LRS', 'Standard_GRS', 'Standard_RAGRS')] $SKU,
    [string]$ResourceGroupName,
    [string]$Location,
    [bool]$ADLSGen2=$false,
    [bool]$AssignIdentity=$true,
    [parameter(Mandatory=$true)]
    [string]$ContainerName
)

Import-Module "$($PSScriptRoot)\Utilities.psm1"

LogInfo "Creating Storage Account [$($AccountName)] in Resource Group [$($ResourceGroupName)]..."

$storageAccount = Get-AzStorageAccount -Name $AccountName -ResourceGroupName $ResourceGroupName -ErrorAction SilentlyContinue

if ($storageAccount -eq $null)
{
    LogInfo "`tStorage Account [$($AccountName)] Does Not Exist.  Creating..."

    $storageAccount = New-AzStorageAccount `
        -Name $AccountName `
        -Location $Location `
        -ResourceGroupName $ResourceGroupName `
        -SkuName $SKU `
        -AccessTier Hot `
        -EnableHttpsTrafficOnly $true `
        -EnableHierarchicalNamespace $ADLSGen2 `
        -Kind StorageV2 `
        -AssignIdentity:$AssignIdentity

    LogInfo "`tStorage Account [$($AccountName)] Created!"
}
else
{
    LogInfo "`tStorage Account [$($AccountName)] Exists.  Moving On!"
}

$storageAccountContext = $storageAccount.Context

LogInfo "Checking if the input blob container exists and, if not, we will create it..."
if((Get-AzRmStorageContainer -ResourceGroupName $ResourceGroupName -StorageAccountName $AccountName -Name $ContainerName -ErrorAction SilentlyContinue) -eq $null)
{
    LogInfo "`tBlob Container $($ContainerName) does not exist. Creating..."

    New-AzStorageContainer `
    -Name $ContainerName `
    -Context $storageAccountContext `
    -Permission blob

    LogInfo "`tBlob Container $($ContainerName) created!"

    LogInfo "`tUploading Data Source files to the $($ContainerName) container..."
}
else
{
    LogInfo "`tBlob Container $($ContainerName) exists. Moving on!"
}

LogInfo "`tUploading data source files to the $($ContainerName)"

$sourceFiles = Get-ChildItem "$($PSScriptRoot)\DataSourceFiles" -Filter *.csv

foreach ($item in $sourceFiles) {
    Set-AzStorageBlobContent `
    -Container $ContainerName `
    -File $item.FullName `
    -Blob "input/$($item.Name)" `
    -Context $storageAccountContext `
    -ErrorAction SilentlyContinue
}

$storageAccountKeys = Get-AzStorageAccountKey -ResourceGroupName $ResourceGroupName -Name $AccountName

$storageAccountKey = $storageAccountKeys[0].Value

Write-Host "##vso[task.setvariable variable=StorageAccount.Key;issecret=true]$($storageAccountKey)"