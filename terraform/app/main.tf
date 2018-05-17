
# ========
# KMS
# ========

resource "aws_kms_key" "key" {
    description = "Used for encrypting AWS Systems Manager Parameters for spectre."
    tags = {
      Group = "ADS"
      Project = "spectre"
      Environment = "prod"
      Client = "ADS"
  }
}

resource "aws_kms_alias" "alias" {
    name = "alias/spectre"
    target_key_id = "${aws_kms_key.key.key_id}"
}

resource "aws_iam_policy" "kms-access-policy" {
  name        = "KMSKeyPolicy-spectre"
  path        = "/"
  description = "Decrypt only access to the spectre KMS key"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": {
    "Effect": "Allow",
    "Action": [
      "kms:Decrypt"
    ],
    "Resource": [
      "${aws_kms_key.key.arn}"
    ]
  }
}
EOF
}

# ==================
# Parameter Store
# ==================

resource "aws_iam_policy" "parameter-store" {
  name        = "parameter-store-spectre"
  path        = "/"
  description = "Read access to all parameters in the AWS System Manager Parameter Store"

  policy  = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
            "ssm:DescribeParameters"
        ],
        "Effect": "Allow",
        "Resource": "*"
      },
      {
        "Action": [
            "ssm:GetParameters"
        ],
        "Effect": "Allow",
        "Resource": [
            "arn:aws:ssm:us-west-2:467892444047:parameter/web-prod.spectre-prod.*"
         ]
      }
  ]
}
EOF
}

# ====================================
# IAM EC2 Container Service Task Roles
# ====================================

resource "aws_iam_role" "spectre" {
  name = "spectre-task"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "s3-kms-decrypt" {
  role       = "${aws_iam_role.spectre.name}"
  policy_arn = "${aws_iam_policy.kms-access-policy.arn}"
}

resource "aws_iam_role_policy_attachment" "parameter-store" {
  role       = "${aws_iam_role.spectre.name}"
  policy_arn = "${aws_iam_policy.parameter-store.arn}"
}


# ====================
# Outputs
# ====================

output "task-role-arn" {
    value = "${aws_iam_role.spectre.arn}"
}

output "kms-key-arn" {
  value = "${aws_kms_key.key.arn}"
}
