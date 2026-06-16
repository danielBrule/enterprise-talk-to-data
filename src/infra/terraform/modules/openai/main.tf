terraform {
  required_providers {
    azapi = {
      source  = "Azure/azapi"
      version = "~> 2.0"
    }
  }
}

resource "azapi_resource" "openai_account" {
  type      = "Microsoft.CognitiveServices/accounts@2024-10-01"
  name      = var.openai_account_name
  location  = var.location
  parent_id = "/subscriptions/${var.subscription_id}/resourceGroups/${var.resource_group_name}"
  tags      = var.tags

  body = {
    kind = "OpenAI"
    sku = {
      name = "S0"
    }
    properties = {
      customSubDomainName = var.openai_account_name
      publicNetworkAccess = "Enabled"
    }
  }
}

resource "azapi_resource" "openai_deployments" {
  for_each = { for d in var.deployment_configs : d.name => d }

  type      = "Microsoft.CognitiveServices/accounts/deployments@2024-10-01"
  name      = each.key
  parent_id = azapi_resource.openai_account.id
  tags      = var.tags

  body = {
    properties = {
      model = {
        format = "OpenAI"
        name   = each.value.model
      }
    }

    sku = {
      name     = "Standard"
      capacity = 1
    }
  }

  depends_on = [azapi_resource.openai_account]
}
