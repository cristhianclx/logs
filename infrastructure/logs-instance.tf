resource "aws_instance" "logs" {
  ami           = data.aws_ami.logs.id
  instance_type = var.logs_instance_size

  vpc_security_group_ids = [aws_security_group.logs.id]
  subnet_id              = aws_default_subnet.a.id

  monitoring = true

  root_block_device {
    volume_type = var.logs_instance_disk_type
    volume_size = var.logs_instance_disk_size
  }

  volume_tags = {
    Name = var.name
  }

  key_name = data.aws_key_pair.key.key_name

  user_data = templatefile("./logs-instance-data.sh", {
    USER                     = var.logs_instance_user,
    PRIVATE_PEM              = templatefile("./../certs/private.pem", {}),
    USER_SSH_AUTHORIZED_KEYS = templatefile("./ssh/id_rsa.pub", {}),
    USER_SSH_CONFIG          = templatefile("./files/home/user/.ssh/config", {}),
    SSH_CONFIG               = templatefile("./files/etc/ssh/sshd_config", {}),
    MOTD                     = templatefile("./files/etc/motd", {}),
    STAGE                    = var.stage,
    REGION                   = data.aws_region.self.name,
    S3                       = "https://${var.logs}.s3.${data.aws_region.self.name}.amazonaws.com"
    LOGS                     = var.logs,
    S3_ACCESS_KEY_ID         = aws_iam_access_key.logs.id,
    S3_SECRET_ACCESS_KEY     = aws_iam_access_key.logs.secret,
  })

  tags = {
    Name = var.logs
  }

  lifecycle {
    ignore_changes = all
  }
}

resource "aws_eip_association" "logs" {
  instance_id         = aws_instance.logs.id
  allocation_id       = aws_eip.logs.id
  allow_reassociation = true

  depends_on = [
    aws_instance.logs,
    aws_eip.logs,
  ]
}
