provider "aws" {
  region  = "ap-northeast-1"
  profile = "my-sso-session"
  skip_credentials_validation = true
  skip_requesting_account_id  = true
  skip_metadata_api_check     = true
  skip_region_validation      = true
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  #backend "s3" {
  #  bucket  = "terraform-state-bucket"
  #  key     = "network-firewall/tokyo.tfstate"
  #  region  = "ap-northeast-1"
  #  profile = "tokyo-profile"
  #}
} 