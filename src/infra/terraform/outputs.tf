output "resource_group_name" {
  description = "The Azure resource group created by Terraform."
  value       = module.resource_group.name
}

output "openai_account_name" {
  description = "The Azure OpenAI account name created by Terraform."
  value       = module.openai.name
}

output "openai_deployment_names" {
  description = "The Azure OpenAI deployments created by Terraform."
  value       = module.openai.deployment_names
}

output "openai_endpoint" {
  description = "Azure OpenAI endpoint."
  value       = module.openai.endpoint
}
