resource "aws_appautoscaling_policy" "service_policy_scale_up" {
  name               = "${local.name}-service-policy-scale-up"
  service_namespace  = aws_appautoscaling_target.service_scale.service_namespace
  resource_id        = aws_appautoscaling_target.service_scale.resource_id
  scalable_dimension = aws_appautoscaling_target.service_scale.scalable_dimension
  step_scaling_policy_configuration {
    adjustment_type         = "ChangeInCapacity"
    cooldown                = 60
    metric_aggregation_type = "Average"
    step_adjustment {
      metric_interval_lower_bound = 0
      scaling_adjustment          = 1
    }
  }
}
resource "aws_appautoscaling_policy" "service_policy_scale_down" {
  name               = "${local.name}-service-policy-scale-down"
  service_namespace  = aws_appautoscaling_target.service_scale.service_namespace
  resource_id        = aws_appautoscaling_target.service_scale.resource_id
  scalable_dimension = aws_appautoscaling_target.service_scale.scalable_dimension
  step_scaling_policy_configuration {
    adjustment_type         = "ChangeInCapacity"
    cooldown                = 300
    metric_aggregation_type = "Average"
    step_adjustment {
      metric_interval_lower_bound = 0
      scaling_adjustment          = -1
    }
  }
}

resource "aws_cloudwatch_metric_alarm" "service_metrics_cpu_utilization_high" {
  alarm_name        = "${local.name}-service-metrics-cpu-utilization-high"
  alarm_description = "${local.name}-service-metrics-cpu-utilization-high"
  alarm_actions = [
    aws_appautoscaling_policy.service_policy_scale_up.arn,
  ]

  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = "60"
  statistic           = "Average"
  threshold           = var.service_metrics_cpu_utilization_high_threshold

  dimensions = {
    ClusterName = var.ecs_name
    ServiceName = aws_ecs_service.service.name
  }
}
resource "aws_cloudwatch_metric_alarm" "service_metrics_cpu_utilization_low" {
  alarm_name        = "${local.name}-service-metrics-cpu-utilization-low"
  alarm_description = "${local.name}-service-metrics-cpu-utilization-low"
  alarm_actions = [
    aws_appautoscaling_policy.service_policy_scale_down.arn,
  ]

  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = "60"
  statistic           = "Average"
  threshold           = var.service_metrics_cpu_utilization_low_threshold

  dimensions = {
    ClusterName = var.ecs_name
    ServiceName = aws_ecs_service.service.name
  }
}

resource "aws_cloudwatch_metric_alarm" "service_metrics_memory_utilization_high" {
  alarm_name        = "${local.name}-service-metrics-memory-utilization-high"
  alarm_description = "${local.name}-service-metrics-memory-utilization-high"
  alarm_actions = [
  ]

  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "MemoryUtilization"
  namespace           = "AWS/ECS"
  period              = "60"
  statistic           = "Average"
  threshold           = var.service_metrics_memory_utilization_high_threshold

  dimensions = {
    ClusterName = var.ecs_name
    ServiceName = aws_ecs_service.service.name
  }
}
