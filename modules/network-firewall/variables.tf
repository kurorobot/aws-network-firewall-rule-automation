variable "region" {
  description = "AWS region"
  type        = string
}

variable "environment_prefix" {
  description = "Environment prefix (e.g., tokyo, singapore, virginia)"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
}

variable "subnet_cidr_a" {
  description = "CIDR block for subnet in AZ a"
  type        = string
}

variable "subnet_cidr_c" {
  description = "CIDR block for subnet in AZ c"
  type        = string
}

variable "firewall_name" {
  description = "Name of the Network Firewall"
  type        = string
}

variable "firewall_policy_name" {
  description = "Name of the Network Firewall Policy"
  type        = string
}

variable "prod_rules_content" {
  description = "Content of the production Suricata rules"
  type        = string
}

variable "nonprod_rules_content" {
  description = "Content of the non-production Suricata rules"
  type        = string
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
} 