variable "stage" {
  description = "stage"
  type        = string
}

variable "name" {
  description = "name"
  type        = string
}
variable "website" {
  description = "website"
  type        = string
}

variable "zone" {
  description = "zone"
  type        = string
}

variable "database_type" {
  description = "database_type"
  type        = string
}
variable "database_version" {
  description = "database_version"
  type        = string
}
variable "database_size" {
  description = "database_size"
  type        = string
}

variable "database_user" {
  description = "database_user"
  type        = string
}
variable "database_password" {
  description = "database_password"
  type        = string
}
variable "database_port" {
  description = "database_port"
  type        = number
}

variable "cache_redis_version" {
  description = "cache_redis_version"
  type        = string
}
variable "cache_redis_size" {
  description = "cache_redis_size"
  type        = string
}
variable "cache_redis_port" {
  description = "cache_redis_port"
  type        = number
}

variable "logs" {
  description = "logs"
  type        = string
}
variable "logs_image_name" {
  description = "logs_image_name"
  type        = string
}
variable "logs_image_owner" {
  description = "logs_image_owner"
  type        = string
}
variable "logs_instance_size" {
  description = "logs_instance_size"
  type        = string
}
variable "logs_instance_disk_type" {
  default     = "gp2"
  description = "logs_instance_disk_type"
  type        = string
}
variable "logs_instance_disk_size" {
  default     = 20
  description = "logs_instance_disk_size"
  type        = number
}
variable "logs_instance_user" {
  description = "logs_instance_user"
  type        = string
}

variable "grafana" {
  description = "grafana"
  type        = string
}
variable "grafana_image_id" {
  description = "grafana_image_id"
  type        = string
}
variable "grafana_instance_size" {
  description = "grafana_instance_size"
  type        = string
}
variable "grafana_instance_disk_type" {
  default     = "gp2"
  description = "grafana_instance_disk_type"
  type        = string
}
variable "grafana_instance_disk_size" {
  description = "grafana_instance_disk_size"
  type        = string
}

variable "ecs_name" {
  description = "ecs_name"
  type        = string
}

variable "service_port" {
  description = "service_port"
  type        = number
}
variable "service_health_check" {
  description = "service_health_check"
  type        = string
}

variable "service_image" {
  description = "service_image"
  type        = string
}
variable "service_cpu" {
  description = "service_cpu"
  type        = number
}
variable "service_memory" {
  description = "service_memory"
  type        = number
}
variable "service_run" {
  description = "service_run"
  type        = string
}

variable "service_metrics_cpu_utilization_high_threshold" {
  description = "service_metrics_cpu_utilization_high_threshold"
  type        = number
}
variable "service_metrics_cpu_utilization_low_threshold" {
  description = "service_metrics_cpu_utilization_low_threshold"
  type        = number
}
variable "service_metrics_memory_utilization_high_threshold" {
  description = "service_metrics_memory_utilization_high_threshold"
  type        = number
}

variable "service_scale_desired" {
  description = "service_scale_desired"
  type        = number
}
variable "service_scale_max" {
  description = "service_scale_max"
  type        = number
}
variable "service_scale_min" {
  description = "service_scale_min"
  type        = number
}
