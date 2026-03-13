# Get default VPC
data "aws_vpc" "default" {
  default = true
}

# Security Group
resource "aws_security_group" "audit_sg" {

  name        = "audit-service-sg"
  description = "Allow SSH and API access"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "API access"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "audit-service-sg"
  }
}

# EC2 Instance
resource "aws_instance" "audit_service" {

  ami           = var.ami_id
  instance_type = var.instance_type

  key_name = "audit-service-key"

  vpc_security_group_ids = [
    aws_security_group.audit_sg.id
  ]

  associate_public_ip_address = true

  user_data = <<-EOF
              #!/bin/bash
              apt update -y
              apt install docker.io git -y

              systemctl start docker
              systemctl enable docker

              cd /home/ubuntu

              git clone https://github.com/Akhil-jagadale/skynet-ops-audit-service.git

              cd skynet-ops-audit-service

              docker build -t audit-service .

              docker run -d -p 3000:3000 audit-service
              EOF

  tags = {
    Name = "skynet-audit-service"
  }
}