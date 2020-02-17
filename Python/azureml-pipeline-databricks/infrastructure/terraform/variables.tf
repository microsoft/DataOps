variable "appname" {
  type = string
  description = "Application name. Use only lowercase letters and numbers"
  default = "myappdataops"
}

variable "environment" {
  type    = string
  description = "Environment name, e.g. 'dev' or 'test'"
  default = "dev"
}

variable "location" {
  type    = string
  description = "Azure region where to create resources."
}

# Service principal Object IDs.
# Should be object IDs of service principals, not object IDs of the application nor application IDs.
# To retrieve, navigate in the AAD portal from an App registration to "Managed application in local directory".

variable "devops_mlpipeline_sp_object_id" {
  type    = string
  description = "Service principal for the Azure DevOps ML Model CI/CD pipeline service connection (e.g. 'DataOpsML Azure DevOps ML Model CI/CD pipeline')"
}
