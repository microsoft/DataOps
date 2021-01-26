# Create virtual network

resource "azurerm_virtual_network" "main" {
  name                = "vnet-${var.appname}-${var.environment}"
  address_space       = ["10.100.0.0/16"]
  location            = var.location
  resource_group_name = var.resource_group_name
}

# Create subnets

resource "azurerm_subnet" "databricks-private" {
  name                 = "databricks-private-subnet"
  resource_group_name = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefix       = "10.100.1.0/24"

  delegation {
    name = "acctestdelegation"
    service_delegation {
      name = "Microsoft.Databricks/workspaces"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/action",
        "Microsoft.Network/virtualNetworks/subnets/join/action",
        "Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action"
      ]
    }
  }
}

resource "azurerm_subnet" "databricks-public" {
  name                 = "databricks-public-subnet"
  resource_group_name = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefix       = "10.100.2.0/24"

  delegation {
    name = "acctestdelegation"
    service_delegation {
      name = "Microsoft.Databricks/workspaces"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/action",
        "Microsoft.Network/virtualNetworks/subnets/join/action",
        "Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action"
      ]
    }
  }
}
