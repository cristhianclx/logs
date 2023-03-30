resource "aws_elasticache_subnet_group" "cache" {
  name        = "${local.name}-cache"
  description = "${local.name}-cache"
  subnet_ids  = local.vpc_private_zone_ids
}

resource "aws_elasticache_cluster" "cache_redis" {
  security_group_ids = [aws_security_group.cache.id]
  subnet_group_name  = aws_elasticache_subnet_group.cache.id

  cluster_id      = "${local.name}-cache-redis"
  engine          = "redis"
  engine_version  = var.cache_redis_version
  node_type       = var.cache_redis_size
  num_cache_nodes = 1

  parameter_group_name = "default.redis7"
  port                 = var.cache_redis_port

  maintenance_window = "sun:00:00-sun:02:00"

  apply_immediately = true
}
