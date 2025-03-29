# VPCの作成
resource "aws_vpc" "network_firewall_vpc" {
  cidr_block = var.vpc_cidr
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = merge(var.tags, {
    Name = "${var.environment_prefix}-network-firewall-vpc"
  })
}

# サブネットの作成 (AZ a)
resource "aws_subnet" "firewall_subnet_a" {
  vpc_id            = aws_vpc.network_firewall_vpc.id
  cidr_block        = var.subnet_cidr_a
  availability_zone = "${var.region}a"
  tags = merge(var.tags, {
    Name = "${var.environment_prefix}-firewall-subnet-a"
  })
}

# サブネットの作成 (AZ c)
resource "aws_subnet" "firewall_subnet_c" {
  vpc_id            = aws_vpc.network_firewall_vpc.id
  cidr_block        = var.subnet_cidr_c
  availability_zone = "${var.region}c"
  tags = merge(var.tags, {
    Name = "${var.environment_prefix}-firewall-subnet-c"
  })
}

# ルール数に基づいて容量を計算
locals {
  prod_rules_content = file("${path.root}/suricata-prod.rules")
  nonprod_rules_content = file("${path.root}/suricata-nonprod.rules")
  
  prod_rules_count = length(regexall("\n", local.prod_rules_content)) + 1
  nonprod_rules_count = length(regexall("\n", local.nonprod_rules_content)) + 1
  
  # 最小容量は100、実際のルール数の2倍を確保
  prod_capacity = max(100, local.prod_rules_count * 2)
  nonprod_capacity = max(100, local.nonprod_rules_count * 2)
}

# プロダクション環境用ルールグループ
resource "aws_networkfirewall_rule_group" "prod" {
  capacity = local.prod_capacity
  name     = "${var.environment_prefix}-network-firewall-rulegroup-stateful-suricata-prod"
  type     = "STATEFUL"
  rule_group {
    rules_source {
      rules_string = local.prod_rules_content
    }
  }

  tags = merge(var.tags, {
    RuleType = "Production"
    Environment = var.environment_prefix
  })
}

# 非プロダクション環境用ルールグループ
resource "aws_networkfirewall_rule_group" "nonprod" {
  capacity = local.nonprod_capacity
  name     = "${var.environment_prefix}-network-firewall-rulegroup-stateful-suricata-nonprod"
  type     = "STATEFUL"
  rule_group {
    rules_source {
      rules_string = local.nonprod_rules_content
    }
  }

  tags = merge(var.tags, {
    RuleType = "NonProduction"
    Environment = var.environment_prefix
  })
}

# Network Firewall の作成
resource "aws_networkfirewall_firewall" "network_firewall" {
  name                = var.firewall_name
  firewall_policy_arn = aws_networkfirewall_firewall_policy.network_firewall_policy.arn
  vpc_id              = aws_vpc.network_firewall_vpc.id
  subnet_mapping {
    subnet_id = aws_subnet.firewall_subnet_a.id
  }
  subnet_mapping {
    subnet_id = aws_subnet.firewall_subnet_c.id
  }

  tags = var.tags
}

# ファイアウォールポリシー
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