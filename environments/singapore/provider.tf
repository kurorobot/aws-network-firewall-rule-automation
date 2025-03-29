provider "aws" {
  region  = "ap-southeast-1"
  profile = "singapore-profile"
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  backend "s3" {
    bucket  = "terraform-state-bucket"
    key     = "network-firewall/singapore.tfstate"
    region  = "ap-southeast-1"
    profile = "singapore-profile"
  }
} 