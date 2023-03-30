resource "aws_route53_record" "website" {
  name    = var.website
  type    = "A"
  zone_id = data.aws_route53_zone.main.zone_id

  alias {
    name                   = aws_alb.alb.dns_name
    zone_id                = aws_alb.alb.zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "logs" {
  name    = var.logs
  type    = "A"
  ttl     = 300
  records = [aws_eip.logs.public_ip]
  zone_id = data.aws_route53_zone.main.zone_id
}

