variable "appname" {
  type = string
  description = "Application name. Use only lowercase letters and numbers"
  default = "mydataops"
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
