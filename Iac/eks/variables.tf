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

variable "cluster_name" {
  default = "plivo_cluster"
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

variable "nodes" {
  description = "no. of worker nodes"
  type = number
  default = 1
}


variable "max_nodes" {
  description = "no. of worker nodes"
  type = number
  default = 5
}

variable "k8s_version" {
  description = "k8s version to use"
  type = string
  default = "1.24"
}
