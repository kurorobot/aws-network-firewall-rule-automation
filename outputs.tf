output "vpc_id" {
  value = aws_vpc.network_firewall_vpc.id
}

output "firewall_id" {
  value = aws_networkfirewall_firewall.network_firewall.id
}

output "firewall_policy_id" {
  value = aws_networkfirewall_firewall_policy.network_firewall_policy.id
}

output "suricata_prod_rules_path" {
  value = "${path.module}/suricata-prod.rules"
}
