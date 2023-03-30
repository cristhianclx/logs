resource "aws_ssm_parameter" "database_host" {
  name        = "/${var.name}/database/host"
  description = "${local.name}-database-host"
  type        = "String"
  value       = aws_db_instance.database.address

  overwrite = true
  tier      = "Standard"
}
resource "aws_ssm_parameter" "database_port" {
  name        = "/${var.name}/database/port"
  description = "${local.name}-database-port"
  type        = "String"
  value       = aws_db_instance.database.port

  overwrite = true
  tier      = "Standard"
}
resource "aws_ssm_parameter" "database_name" {
  name        = "/${var.name}/database/name"
  description = "${local.name}-database-name"
  type        = "String"
  value       = aws_db_instance.database.db_name

  overwrite = true
  tier      = "Standard"
}
resource "aws_ssm_parameter" "database_user" {
  name        = "/${var.name}/database/user"
  description = "${local.name}-database-user"
  type        = "String"
  value       = aws_db_instance.database.username

  overwrite = true
  tier      = "Standard"
}
resource "aws_ssm_parameter" "database_password" {
  name        = "/${var.name}/database/password"
  description = "${local.name}-database-password"
  type        = "SecureString"
  value       = aws_db_instance.database.password

  key_id    = "alias/aws/ssm"
  overwrite = true
  tier      = "Standard"
}
