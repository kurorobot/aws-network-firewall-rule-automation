variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "ap-northeast-3"
}

variable "vpc_cidr" {
  description = "VPCのCIDRブロック"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr_a" {
  description = "Firewall Subnet (ap-northeast-3a)"
  type        = string
  default     = "10.0.1.0/24"
}

variable "subnet_cidr_c" {
  description = "Firewall Subnet (ap-northeast-3c)"
  type        = string
  default     = "10.0.2.0/24"
}

variable "firewall_policy_name" {
  description = "Firewall Policy Name"
  type        = string
  default     = "network-firewall-policy"
}

variable "firewall_name" {
  description = "Firewall Name"
  type        = string
  default     = "network-firewall"
}

variable "tags" {
  description = "Resource Tags"
  type        = map(string)
  default = {
    Owner       = "CCoE"
    Environment = "ccoe-network-firewall"
  }
}
