data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "audit_sg" {
  name   = "audit-service-sg"
  vpc_id = data.aws_vpc.default.id

  ingress {
    description = "SSH Access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Audit API"
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


resource "aws_instance" "audit_service" {

  ami           = var.ami_id
  instance_type = var.instance_type

  key_name = "audit-service-key"

  vpc_security_group_ids = [aws_security_group.audit_sg.id]

  associate_public_ip_address = true

  tags = {
    Name = "skynet-audit-service"
  }
}