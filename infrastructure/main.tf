terraform {
  required_version = ">=1.4.2"

  backend "s3" {
    bucket               = "infrastructure.demo.pe"
    key                  = "logs.demo.pe"
    encrypt              = "true"
    region               = "sa-east-1"
    workspace_key_prefix = "tf"
  }
}
