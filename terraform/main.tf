provider "aws" {
  region = "eu-west-3" 
}

resource "aws_key_pair" "deployer" {
  key_name   = "lyonvaycay-ssh-key"
  public_key = file("~/.ssh/lyonvaycay_key.pub")
}

resource "aws_security_group" "lyon_web_sg" {
  name        = "lyon-vaycay-web-sg"
  description = "Allow web and SSH traffic"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "lyon_server" {
  ami           = "ami-00ac45f3035ff009e" # Ubuntu 22.04 LTS
  instance_type = "t3.micro"              # Free Tier
  
  key_name = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.lyon_web_sg.id]

  tags = {
    Name = "LyonVaycay-Production"
  }
}

output "server_ip" {
  value = aws_instance.lyon_server.public_ip
}