# docker
resource "aws_ecr_repository" "main" {
  name = var.website
}

# docker-policy
resource "aws_ecr_lifecycle_policy" "api_policy" {
  repository = aws_ecr_repository.main.name

  policy = templatefile("./ecr-policy.json", {
    ecr_policy_expire_days = 30
  })
}
