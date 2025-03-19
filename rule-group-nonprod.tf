resource "aws_networkfirewall_rule_group" "nonprod" {
  capacity = 10000
  name     = "network-firewall-rulegroup-stateful-suricata-nonprod"
  type     = "STATEFUL"
  rule_group {
    rules_source {
      rules_string = file("${path.module}/suricata-nonprod.rules")
    }
  }

  tags = var.tags
}
