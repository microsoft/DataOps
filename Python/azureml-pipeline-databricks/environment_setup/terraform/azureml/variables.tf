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

variable "object_id" {
  type    = string
}

variable "devops_mlpipeline_sp_object_id" {
  type    = string
  description = "Service principal object ID for the Azure DevOps ML Model CI/CD pipeline service connection"
}
