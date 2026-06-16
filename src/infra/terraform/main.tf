locals {
  environment         = lower(trimspace(var.environment))
  resource_group_name = length(trimspace(var.resource_group_name)) > 0 ? var.resource_group_name : "rg-lefigaro-talk2data-${local.environment}"
  openai_account_name = length(trimspace(var.openai_account_name)) > 0 ? var.openai_account_name : "openai-lefigaro-${local.environment}"

  openai_deployments = [
    {
      name  = "talk2data-gpt41mini-schema-retrieval"
      model = var.schema_retrieval_model
    },
    {
      name  = "talk2data-gpt41mini-sql-generation"
      model = var.sql_generation_model
    },
    {
      name  = "talk2data-gpt41mini-summary"
      model = var.summary_model
    },
  ]
}

module "resource_group" {
  source              = "./modules/resource_group"
  resource_group_name = local.resource_group_name
  location            = var.location
  tags = {
    environment = local.environment
    project     = "lefigaro-talk2data"
  }
}

module "openai" {
  source              = "./modules/openai"
  subscription_id     = var.subscription_id
  resource_group_name = module.resource_group.name
  location            = var.location
  openai_account_name = local.openai_account_name
  deployment_configs  = local.openai_deployments
  tags = {
    environment = local.environment
    project     = "lefigaro-talk2data"
  }
}
