locals {
  workspace_to_region_map = {
    tokyo     = "ap-northeast-1"
    singapore = "ap-southeast-1"
    virginia  = "us-east-1"
  }
  
  workspace_to_profile_map = {
    tokyo     = "my-sso-session"
    singapore = "singapore-profile"
    virginia  = "virginia-profile"
  }
  
  region  = local.workspace_to_region_map[terraform.workspace]
  profile = local.workspace_to_profile_map[terraform.workspace]
}

provider "aws" {
  region  = local.region
  profile = local.profile
}

terraform {
  backend "s3" {
    bucket  = "terraform-state-bucket"
    key     = "network-firewall/terraform.tfstate"
    region  = "ap-northeast-1"
    # 注意: バックエンドの設定ではワークスペース変数を使用できないため、
    # terraform init -backend-config="profile=xxx" のように指定する必要がある
  }
}