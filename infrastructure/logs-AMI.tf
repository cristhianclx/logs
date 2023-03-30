data "aws_ami" "logs" {
  filter {
    name   = "name"
    values = [var.logs_image_name]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  owners      = [var.logs_image_owner]
  most_recent = true
}
