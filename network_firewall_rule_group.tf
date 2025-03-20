resource "aws_networkfirewall_rule_group" "network_firewall_suricata_rules" {
  capacity = 100
  name     = "network-firewall-rulegroup-stateful-suricata-prod"
  type     = "STATEFUL"
  
  rule_group {
    rules_source {
      rules_string = <<EOT
# ここに初期ルールを記述（空でも可）
EOT
    }
  }
  
  tags = {
    Name = "network-firewall-rulegroup-stateful-suricata-prod"
  }
} 