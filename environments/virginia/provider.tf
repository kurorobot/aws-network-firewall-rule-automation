provider "aws" {
  region  = "us-east-1"
  profile = "virginia-profile"
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
    key     = "network-firewall/virginia.tfstate"
    region  = "us-east-1"
    profile = "virginia-profile"
  }
} 