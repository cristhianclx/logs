resource "aws_security_group" "cache" {
  name        = "${local.name}-cache"
  description = "${local.name}-cache"
  vpc_id      = local.vpc_id

  tags = {
    Name = "${local.name}-cache"
  }
}

resource "aws_security_group_rule" "cache_ingress_tasks" {
  security_group_id = aws_security_group.cache.id

  type = "ingress"

  from_port                = var.cache_redis_port
  to_port                  = var.cache_redis_port
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.tasks.id
}

resource "aws_security_group_rule" "cache_egress" {
  security_group_id = aws_security_group.cache.id

  type = "egress"

  from_port   = 0
  to_port     = 65535
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}
