variable "aws_region" {
  default = "ap-south-1"
}

variable "aws_profile" {
  description = "which aws cli profile to be used"
  default = "plivo"
}

variable "project_name" {
  default = "plivo"
}

variable "primary_vpc_cidr" {
  description = "Primary CIDR to be used by the VPC"
  type = string
  default = "10.81.0.0/16"
}

variable "secondary_vpc_cidr" {
  description = "Primary CIDR to be used by the VPC"
  type = string
  default = "10.82.0.0/16"
}

variable "secret_key" {
  description = "secret-key"
  type = string
  
}

variable "access_key" {
  description = "access-key"
  type = string
  
}