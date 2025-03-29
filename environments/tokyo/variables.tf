variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-1"
}

variable "environment_prefix" {
  description = "Environment prefix"
  type        = string
  default     = "tokyo"
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

variable "prod_rules_file" {
  description = "Path to the production Suricata rules file"
  type        = string
  default     = "suricata-prod.rules"
}

variable "nonprod_rules_file" {
  description = "Path to the non-production Suricata rules file"
  type        = string
  default     = "suricata-nonprod.rules"
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {
    Environment = "Tokyo"
    ManagedBy   = "Terraform"
  }
} 