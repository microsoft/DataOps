output "vnet_name" {
  value = azurerm_virtual_network.main.name
}

output "databricks_private_subnet_name" {
  value = azurerm_subnet.databricks-private.name
}

output "databricks_public_subnet_name" {
  value = azurerm_subnet.databricks-public.name
}
