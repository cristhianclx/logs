resource "aws_ssm_parameter" "logs_host" {
  name        = "/${var.name}/logs/host"
  description = "${local.name}-logs-host"
  type        = "String"
  value       = aws_eip.logs.public_ip

  overwrite = true
  tier      = "Standard"
}
resource "aws_ssm_parameter" "logs_port" {
  name        = "/${var.name}/logs/port"
  description = "${local.name}-logs-port"
  type        = "String"
  value       = 3322

  overwrite = true
  tier      = "Standard"
}
