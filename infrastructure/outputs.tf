output "name" {
  value = var.name
}
output "stage" {
  value = var.stage
}
output "website" {
  value = aws_route53_record.website.fqdn
}
