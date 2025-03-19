resource "aws_networkfirewall_firewall_policy" "network_firewall_policy" {
  name = var.firewall_policy_name

  firewall_policy {
    stateless_default_actions          = ["aws:drop"]
    stateless_fragment_default_actions = ["aws:drop"]

    stateful_rule_group_reference {
      resource_arn = aws_networkfirewall_rule_group.prod.arn
    }

    stateful_rule_group_reference {
      resource_arn = aws_networkfirewall_rule_group.nonprod.arn
    }
  }

  tags = var.tags
}
