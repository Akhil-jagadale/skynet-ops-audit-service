output "instance_public_ip" {
  value = aws_instance.audit_service.public_ip
}