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

# The total number of characters of the appname and environment variables additioned
# Should not exceed 8 characters

variable "location" {
  type    = string
  description = "Azure region where to create resources."
}
