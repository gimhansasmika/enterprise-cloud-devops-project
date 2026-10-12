
# ============================================
# Enterprise Cloud Infrastructure Project
# Terraform Read-Only Infrastructure Inspection
# AWS Region: Asia Pacific (Sydney)
# ============================================

# 1. Terraform Configuration

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# 2. AWS Provider Configuration

provider "aws" {
  region = "ap-southeast-2"
}

# 3. Read Existing AWS VPC

data "aws_vpc" "enterprise" {
  id = "vpc-08763a69ef2291556"
}

# 4. VPC Information Outputs

output "enterprise_vpc_id" {
  description = "Existing Enterprise VPC ID"
  value       = data.aws_vpc.enterprise.id
}

output "enterprise_vpc_cidr" {
  description = "Enterprise VPC CIDR Block"
  value       = data.aws_vpc.enterprise.cidr_block
}

output "enterprise_vpc_state" {
  description = "Current Enterprise VPC State"
  value       = data.aws_vpc.enterprise.state
}

output "enterprise_vpc_name" {
  description = "Enterprise VPC Name"
  value       = data.aws_vpc.enterprise.tags["Name"]
}
