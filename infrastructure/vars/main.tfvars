stage = "main"

name    = "logs.demo.pe/main"
website = "logs.demo.pe"

zone = "demo.pe"

database_type    = "postgres"
database_version = "15.2"
database_size    = "db.t3.micro"

database_user     = "api"
database_password = "password"
database_port     = 5432

cache_redis_version = "7.0"
cache_redis_size    = "cache.t3.micro"
cache_redis_port    = 6379

logs                    = "store.logs.demo.pe"
logs_image_name         = "debian-11-amd64-*"
logs_image_owner        = "679593333241"
logs_instance_size      = "t3.small"
logs_instance_disk_size = 50
logs_instance_user      = "cristhian"

grafana                    = "grafana.logs.demo.pe"
grafana_image_id           = "ami-070802b0ef8efdff7"
grafana_instance_size      = "t3.small"
grafana_instance_disk_size = 50

ecs_name = "main"

service_port         = 8000
service_health_check = "/ping/"

service_image  = "263424986970.dkr.ecr.us-east-1.amazonaws.com/logs.demo.pe:main"
service_cpu    = 256
service_memory = 512
service_run    = "/code/scripts/settings/main.sh && /code/scripts/migrate.sh && /code/scripts/seed.sh && /code/scripts/run.sh"

service_metrics_cpu_utilization_high_threshold    = 80
service_metrics_cpu_utilization_low_threshold     = 20
service_metrics_memory_utilization_high_threshold = 80

service_scale_desired = 1
service_scale_max     = 1
service_scale_min     = 1
