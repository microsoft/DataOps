variable "appname" {
  type = string
}

variable "environment" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "location" {
  type    = string
}

variable "tenant_id" {
  type    = string
}

variable "devops_mlpipeline_sp_object_id" {
  type    = string
  description = "Service principal object ID for the Azure DevOps ML Model CI/CD pipeline service connection"
}

variable "devops_mlpipeline_sp_client_id" {
  type    = string
  description = "Service principal client ID for the Azure DevOps ML Model CI/CD pipeline service connection"
}

variable "devops_mlpipeline_sp_client_secret" {
  type    = string
  description = "Service principal client secret for the Azure DevOps ML Model CI/CD pipeline service connection"
}
