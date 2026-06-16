output "name" {
  description = "OpenAI account name."
  value       = azapi_resource.openai_account.name
}

output "id" {
  description = "OpenAI account resource ID."
  value       = azapi_resource.openai_account.id
}

output "deployment_names" {
  description = "Names of created OpenAI deployments."
  value       = keys(azapi_resource.openai_deployments)
}

output "endpoint" {
  description = "Azure OpenAI endpoint."
  value       = "https://${azapi_resource.openai_account.name}.openai.azure.com/"
}
