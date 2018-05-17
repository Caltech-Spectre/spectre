variable "region" {
  default = "us-west-2"
}

provider "aws" {
  region = "${var.region}"
}

terraform {
  backend "s3" {
    key     = "spectre-terraform-state"
    bucket  = "caltech-terraform-remotestate-file"
    region  = "us-west-2"
  }
}

# VPC infrastructure statefile
data "terraform_remote_state" "vpc" {
  backend = "s3"

  config {
    key    = "ads-web-terraform-state"
    bucket = "caltech-terraform-remotestate-file"
    region = "us-west-2"
  }
}

# ==================
# ECR Repository
# ==================
resource "aws_ecr_repository" "spectre" {
  name = "caltech-imss-ads/spectre"
}

# ====================================
# IAM Roles and KMS keys
# ====================================

# the test1 environment is ADS' environment for testing the
# access.caltech-testservers build.  The CodePipeline deploy deploys to this
# environment. 

module "prod" {
    source                           = "./app"
}

# ================
# Outputs: test1
# ================

output "test1-task-role-arn" {
  value = "${module.prod.task-role-arn}"
}

output "test1-kms-key-arn" {
  value = "${module.prod.kms-key-arn}"
}

# ==================
# Outputs: General
# ==================

output "ecr_repository" {
  value = "${aws_ecr_repository.spectre.repository_url}"
}

output "ecs-cluster-name" {
  value = "${data.terraform_remote_state.vpc.ecs-web-prod-cluster-name}"
}

output "rds-address" {
  value = "${data.terraform_remote_state.vpc.rds-prod-address}"
}

output "rds-port" {
  value = "${data.terraform_remote_state.vpc.rds-prod-port}"
}

output "task-role-arn" {
  value = "${module.prod.task-role-arn}"
}