# ECR repo
resource "aws_ecr_repository" "app" {
  name                 = "prod-app"
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecr_repository" "db" {
  name                 = "prod-db"
  image_tag_mutability = "MUTABLE"
}

# S3 bucket to store images
resource "aws_s3_bucket" "assets" {
  bucket = "clo835-group8-website-assets"
}

# # IAM policy to be used by EKS role for IRSA
# resource "aws_iam_policy" "s3_read_policy" {
#   name        = "EKS_S3ReadPolicy"
#   description = "Policy to allow read access to the S3 bucket where background image is stored"
#   policy      = jsonencode({
#     Version = "2012-10-17",
#     Statement = [{
#       Effect = "Allow",
#       Action = [
#         "s3:GetObject",
#         "s3:ListBucket",
#       ],
#       Resource = [
#         "arn:aws:s3:::${aws_s3_bucket.assets.id}",
#         "arn:aws:s3:::${aws_s3_bucket.assets.id}/*"
#       ],
#     }]
#   })
# }

# # IAM role to be used by EKS for IRSA
# resource "aws_iam_role" "eks_service_role" {
#   name = "EKS_ServiceRole"

#   assume_role_policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [{
#       Effect = "Allow",
#       Principal = {
#         Service = "eks.amazonaws.com"
#       },
#       Action = "sts:AssumeRole",
#     }]
#   })
# }

# resource "aws_iam_role_policy_attachment" "s3_read_policy_attachment" {
#   policy_arn = aws_iam_policy.s3_read_policy.arn
#   role       = aws_iam_role.eks_service_role.name
# }

# output "iam_role_arn" {
#   value = aws_iam_role.eks_service_role.arn
# }
