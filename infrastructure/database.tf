data "aws_kms_alias" "rds" {
  name = "alias/aws/rds"
}

resource "aws_db_subnet_group" "database" {
  name       = "${local.name}-database"
  subnet_ids = local.vpc_private_zone_ids

  tags = {
    Name = "${local.name}-database"
  }
}

resource "aws_db_instance" "database" {
  vpc_security_group_ids = [aws_security_group.database.id]
  db_subnet_group_name   = aws_db_subnet_group.database.id

  allocated_storage     = 20
  max_allocated_storage = 100
  storage_encrypted     = false
  storage_type          = "gp2"

  multi_az                    = false
  allow_major_version_upgrade = true
  skip_final_snapshot         = true

  identifier     = "${local.name}-database"
  engine         = var.database_type
  engine_version = var.database_version
  instance_class = var.database_size

  db_name  = "bbdd"
  username = var.database_user
  password = var.database_password
  port     = var.database_port

  backup_retention_period = 14
  backup_window           = "02:30-04:30"
  copy_tags_to_snapshot   = true
  maintenance_window      = "sun:00:00-sun:02:00"

  monitoring_interval = 30
  monitoring_role_arn = aws_iam_role.rds_monitoring_role.arn

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  performance_insights_enabled          = true
  performance_insights_kms_key_id       = data.aws_kms_alias.rds.target_key_arn
  performance_insights_retention_period = 7

  apply_immediately   = true
  deletion_protection = false
  publicly_accessible = false

  tags = {
    Name = "${local.name}-database"
  }

  depends_on = [
    aws_security_group.database,
  ]
}
