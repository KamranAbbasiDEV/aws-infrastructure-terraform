output "instance_id" {
  description = "EC2 instance ID."
  value       = aws_instance.web.id
}

output "public_ip" {
  description = "Public IP assigned to the EC2 lab instance."
  value       = aws_instance.web.public_ip
}

output "http_url" {
  description = "HTTP-only lab website (not a production HTTPS endpoint)."
  value       = "http://${aws_instance.web.public_ip}"
}

output "ssm_start_session_command" {
  description = "Use an authorized AWS CLI profile to connect without SSH."
  value       = "aws ssm start-session --target ${aws_instance.web.id} --region ${var.aws_region}"
}
