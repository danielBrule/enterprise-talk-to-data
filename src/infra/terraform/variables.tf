variable "environment" {
  type        = string
  description = "Deployment environment name, such as dev or prod."
  default     = "dev"
}

variable "location" {
  type        = string
  description = "Azure region for resources."
  default     = "eastus"
}

variable "subscription_id" {
  type        = string
  description = "Azure subscription ID for the target deployment."
}

variable "tenant_id" {
  type        = string
  description = "Azure tenant ID for the target deployment."
}

variable "client_id" {
  type        = string
  description = "Azure service principal client ID."
}

variable "user_object_id" {
  type        = string
  description = "Azure user object ID for access control or RBAC."
}

variable "image_tag" {
  type        = string
  description = "Environment image tag for deployment or metadata settings."
  default     = "dev"
}

variable "resource_group_name" {
  type        = string
  description = "Optional explicit resource group name. If empty, it is derived from the environment."
  default     = ""
}

variable "openai_account_name" {
  type        = string
  description = "Optional explicit OpenAI account name. If empty, it is derived from the environment."
  default     = ""
}

variable "schema_retrieval_model" {
  type        = string
  description = "Model to use for schema retrieval."
  default     = "gpt-4.1-mini"
}

variable "sql_generation_model" {
  type        = string
  description = "Model to use for SQL generation."
  default     = "gpt-4.1-mini"
}

variable "summary_model" {
  type        = string
  description = "Model to use for summarizing results."
  default     = "gpt-4.1-mini"
}
