module "network_firewall" {
  source = "../../modules/network-firewall"

  region             = var.region
  environment_prefix = var.environment_prefix
  vpc_cidr           = var.vpc_cidr
  subnet_cidr_a      = var.subnet_cidr_a
  subnet_cidr_c      = var.subnet_cidr_c
  firewall_name      = var.firewall_name
  firewall_policy_name = var.firewall_policy_name
  tags               = var.tags
} 