resource "azurerm_storage_account" "training_data" {
  name                     = "st${var.appname}tr${var.environment}"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_kind             = "StorageV2"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "training_data" {
  name                  = "trainingdata"
  storage_account_name  = azurerm_storage_account.training_data.name
}

resource "azurerm_storage_blob" "training_data" {
  name                  = "diabetes.csv"
  storage_account_name   = azurerm_storage_account.training_data.name
  storage_container_name = azurerm_storage_container.training_data.name
  type                   = "Block"
  source                 = "${path.module}/diabetes.csv"
}
