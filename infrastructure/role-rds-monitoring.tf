data "aws_iam_policy_document" "rds_monitoring_role_assume_policy" {
  statement {
    actions = [
      "sts:AssumeRole"
    ]
    effect = "Allow"
    principals {
      identifiers = [
        "monitoring.rds.amazonaws.com"
      ]
      type = "Service"
    }
  }
}

resource "aws_iam_role" "rds_monitoring_role" {
  assume_role_policy = data.aws_iam_policy_document.rds_monitoring_role_assume_policy.json

  name                  = "${local.name}-rds-monitoring-role"
  description           = "rds-monitoring-role"
  force_detach_policies = true
}

resource "aws_iam_role_policy_attachment" "rds_monitoring_role_policy_rds_enhanced_monitoring_role" {
  role       = aws_iam_role.rds_monitoring_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}
