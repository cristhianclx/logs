resource "aws_eip" "logs" {
  vpc = true

  tags = {
    Name = var.logs
  }
}
