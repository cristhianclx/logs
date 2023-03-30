resource "aws_ecs_task_definition" "service" {
  family = "${local.name}-service"

  execution_role_arn = aws_iam_role.ecs_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_role.arn

  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]

  cpu    = var.service_cpu
  memory = var.service_memory

  container_definitions = templatefile("./ecs-service.json", {
    logs_name      = var.name,
    logs_region    = data.aws_region.self.name,
    name           = local.name,
    service_image  = var.service_image,
    service_cpu    = var.service_cpu,
    service_memory = var.service_memory,
    service_run    = var.service_run,
    service_port   = var.service_port,
  })

  lifecycle {
    ignore_changes = [
      cpu,
      memory,
      container_definitions,
    ]
  }
}

resource "aws_ecs_service" "service" {
  name = "${local.name}-service"

  cluster         = aws_ecs_cluster.main.arn
  launch_type     = "FARGATE"
  task_definition = aws_ecs_task_definition.service.arn
  desired_count   = var.service_scale_desired

  network_configuration {
    security_groups  = [aws_security_group.tasks.id]
    subnets          = local.vpc_public_zone_ids
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.service.id
    container_name   = "${local.name}-service"
    container_port   = var.service_port
  }

  depends_on = [
    aws_alb_listener.alb_http,
    aws_alb_listener.alb_https,
  ]

  lifecycle {
    ignore_changes = [
      task_definition,
      desired_count,
    ]
  }
}

resource "aws_appautoscaling_target" "service_scale" {
  service_namespace = "ecs"
  resource_id       = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.service.name}"

  scalable_dimension = "ecs:service:DesiredCount"
  max_capacity       = var.service_scale_max
  min_capacity       = var.service_scale_min
}
