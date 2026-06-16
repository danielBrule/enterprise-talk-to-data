variable "resource_group_name" {
  type        = string
  description = "Name of the Azure resource group."
}

variable "location" {
  type        = string
  description = "Azure region for the resource group."
}

variable "tags" {
  type        = map(string)
  description = "Tags to assign to the resource group."
  default     = {}
}
