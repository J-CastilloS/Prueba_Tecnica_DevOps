module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "transcription-eks-cluster"
  cluster_version = "1.27"
  subnets         = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id

  node_groups = {
    eks_nodes = {
      desired_capacity = 2
      max_capacity     = 4
      min_capacity     = 1

      instance_type = "t3.medium"
    }
  }

  tags = {
    Environment = "Development"
  }
}