resource "aws_security_group" "database" {
  name        = "${local.name}-database"
  description = "${local.name}-database"
  vpc_id      = local.vpc_id

  tags = {
    Name = "${local.name}-database"
  }
}

resource "aws_security_group_rule" "database_ingress_tasks" {
  security_group_id = aws_security_group.database.id

  type = "ingress"

  from_port                = var.database_port
  to_port                  = var.database_port
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.tasks.id
}

resource "aws_security_group_rule" "database_egress" {
  security_group_id = aws_security_group.database.id

  type = "egress"

  from_port   = 0
  to_port     = 65535
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}
