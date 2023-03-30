resource "aws_alb" "alb" {
  name               = "${local.name}-alb"
  subnets            = local.vpc_public_zone_ids
  security_groups    = [aws_security_group.alb.id]
  load_balancer_type = "application"
  idle_timeout       = 300
  enable_http2       = true
}

resource "aws_alb_listener" "alb_http" {
  load_balancer_arn = aws_alb.alb.id
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.service.id
  }
}
resource "aws_alb_listener" "alb_https" {
  load_balancer_arn = aws_alb.alb.id
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = data.aws_acm_certificate.main.arn
  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.service.id
  }
}

resource "aws_alb_target_group" "service" {
  name                 = "${local.name}-service"
  port                 = var.service_port
  protocol             = "HTTP"
  vpc_id               = local.vpc_id
  target_type          = "ip"
  deregistration_delay = 300
  health_check {
    path                = var.service_health_check
    matcher             = "200"
    interval            = "30"
    timeout             = "10"
    protocol            = "HTTP"
    port                = var.service_port
    healthy_threshold   = 2
    unhealthy_threshold = 10
  }
}
