resource "aws_instance" "ml_ec2" {
  ami           = "ami-0e472ba40eb589f49" # Amazon Linux 2 with GPU support
  instance_type = "g4dn.xlarge"
  subnet_id     = module.vpc.public_subnets[0]

  tags = {
    Name = "ML-Instance"
  }

  user_data = <<-EOF
                #!/bin/bash
                yum update -y
                yum install -y aws-cli docker
                service docker start
              EOF
}