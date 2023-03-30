resource "aws_ssm_parameter" "cache_host" {
  name        = "/${var.name}/cache/host"
  description = "${local.name}-cache-host"
  type        = "String"
  value       = aws_elasticache_cluster.cache_redis.cache_nodes[0].address

  overwrite = true
  tier      = "Standard"
}
resource "aws_ssm_parameter" "cache_port" {
  name        = "/${var.name}/cache/port"
  description = "${local.name}-cache-port"
  type        = "String"
  value       = aws_elasticache_cluster.cache_redis.cache_nodes[0].port

  overwrite = true
  tier      = "Standard"
}
