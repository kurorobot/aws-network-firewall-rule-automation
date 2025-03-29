output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.network_firewall_vpc.id
}

output "firewall_id" {
  description = "ID of the created Network Firewall"
  value       = aws_networkfirewall_firewall.network_firewall.id
}

output "prod_rule_group_arn" {
  description = "ARN of the production rule group"
  value       = aws_networkfirewall_rule_group.prod.arn
}

output "nonprod_rule_group_arn" {
  description = "ARN of the non-production rule group"
  value       = aws_networkfirewall_rule_group.nonprod.arn
}

output "firewall_policy_arn" {
  description = "ARN of the firewall policy"
  value       = aws_networkfirewall_firewall_policy.network_firewall_policy.arn
} 