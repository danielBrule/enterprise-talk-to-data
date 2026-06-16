variable "subscription_id" {
  type        = string
  description = "The Azure subscription ID."
}

variable "resource_group_name" {
  type        = string
  description = "The target resource group name for the OpenAI account."
}

variable "location" {
  type        = string
  description = "Azure region for the OpenAI account."
}

variable "openai_account_name" {
  type        = string
  description = "The Azure OpenAI account name."
}

variable "deployment_configs" {
  type = list(object({
    name  = string
    model = string
  }))
  description = "List of OpenAI deployments to create."
}

variable "tags" {
  type        = map(string)
  description = "Tags to assign to the OpenAI account and deployments."
  default     = {}
}
