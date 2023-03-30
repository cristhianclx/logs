resource "aws_default_vpc" "main" {
  tags = {
    Name = "vpc"
  }
}

resource "aws_default_subnet" "a" {
  availability_zone = "us-east-1a"
  tags = {
    Name = "vpc-a"
  }
}
resource "aws_default_subnet" "b" {
  availability_zone = "us-east-1b"
  tags = {
    Name = "vpc-b"
  }
}
resource "aws_default_subnet" "c" {
  availability_zone = "us-east-1c"
  tags = {
    Name = "vpc-c"
  }
}
