# VPCの作成
resource "aws_vpc" "network_firewall_vpc" {
  cidr_block = var.vpc_cidr
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = merge(var.tags, {
    Name = "network-firewall-vpc"
  })
}

# サブネットの作成 (ap-northeast-3a)
resource "aws_subnet" "firewall_subnet_a" {
  vpc_id            = aws_vpc.network_firewall_vpc.id
  cidr_block        = var.subnet_cidr_a
  availability_zone = "ap-northeast-3a"
  tags = merge(var.tags, {
    Name = "firewall-subnet-a"
  })
}

# サブネットの作成 (ap-northeast-3c)
resource "aws_subnet" "firewall_subnet_c" {
  vpc_id            = aws_vpc.network_firewall_vpc.id
  cidr_block        = var.subnet_cidr_c
  availability_zone = "ap-northeast-3c"
  tags = merge(var.tags, {
    Name = "firewall-subnet-c"
  })
}

# Network Firewall の作成
resource "aws_networkfirewall_firewall" "network_firewall" {
  name                = var.firewall_name
  firewall_policy_arn = aws_networkfirewall_firewall_policy.network_firewall_policy.arn
  vpc_id             = aws_vpc.network_firewall_vpc.id
  subnet_mapping {
    subnet_id = aws_subnet.firewall_subnet_a.id
  }
  subnet_mapping {
    subnet_id = aws_subnet.firewall_subnet_c.id
  }

  tags = var.tags
}
