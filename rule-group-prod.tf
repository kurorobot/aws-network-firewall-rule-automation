resource "aws_networkfirewall_rule_group" "prod" {
  capacity = 10000
  name     = "network-firewall-rulegroup-stateful-suricata-prod"
  type     = "STATEFUL"
  rule_group {
    rules_source {
      rules_string = file("${path.module}/suricata-prod.rules")
    }
  }

  tags = var.tags
}
