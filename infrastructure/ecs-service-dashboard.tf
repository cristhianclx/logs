resource "aws_cloudwatch_dashboard" "service" {
  dashboard_name = local.name
  dashboard_body = templatefile("./ecs-service-dashboard.json", {
    service_name                            = aws_ecs_service.service.name,
    cluster_name                            = var.ecs_name,
    region                                  = data.aws_region.self.name,
    aws_alb_target_group_service_arn_suffix = aws_alb_target_group.service.arn_suffix,
    aws_alb_service_arn_suffix              = aws_alb.alb.arn_suffix,
  })
}
