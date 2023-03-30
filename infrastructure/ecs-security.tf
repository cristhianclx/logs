resource "aws_security_group" "tasks" {
  name        = "${local.name}-tasks"
  description = "${local.name}-tasks"
  vpc_id      = local.vpc_id

  ingress {
    protocol        = "tcp"
    from_port       = var.service_port
    to_port         = var.service_port
    security_groups = [aws_security_group.alb.id]
  }
  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${local.name}-tasks"
  }
}
