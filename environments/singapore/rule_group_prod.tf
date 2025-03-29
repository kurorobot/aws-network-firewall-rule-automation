# ルールグループのみを更新するためのTerraformファイル
resource "aws_networkfirewall_rule_group" "prod" {
  capacity = 100
  name     = "singapore-network-firewall-rulegroup-stateful-suricata-prod"
  type     = "STATEFUL"
  
  rule_group {
    rules_source {
      rules_string = file("${path.module}/suricata-prod.rules")
    }
  }
  
  tags = {
    Name = "singapore-network-firewall-rulegroup-stateful-suricata-prod"
    Environment = "prod"
    Region = "singapore"
  }
} 