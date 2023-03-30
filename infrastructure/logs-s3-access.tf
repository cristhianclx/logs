resource "aws_iam_user" "logs" {
  name = "${local.logs}-${var.stage}"
}
resource "aws_iam_access_key" "logs" {
  user = aws_iam_user.logs.name
}

resource "aws_iam_user_policy_attachment" "logs_s3_full_access" {
  user       = aws_iam_user.logs.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}
