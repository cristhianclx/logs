data "aws_acm_certificate" "main" {
  domain   = var.zone
  statuses = ["ISSUED"]
}
data "aws_region" "self" {}
data "aws_route53_zone" "main" {
  name         = var.zone
  private_zone = false
}
data "aws_key_pair" "key" {
  key_name           = var.website
  include_public_key = false
}
