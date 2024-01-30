module "network" {
  source = "../networks"
  # access_key = var.access_key
  # secret_key = var.secret_key
}

module "policy" {
  source = "../policy"
  # access_key = var.access_key
  # secret_key = var.secret_key
}

resource "aws_eks_cluster" "plivo-cluster" {
  name     = var.cluster_name
  role_arn = module.policy.plivo-cluster-role
  version = var.k8s_version
  vpc_config {
    subnet_ids = [
      module.network.subnet-1,
      module.network.subnet-2,
      module.network.subnet-3
    ]
  }

  depends_on = [module.policy.plivo-cluster-role, module.network.subnet-1]
}

resource "aws_eks_node_group" "private-nodes" {
  cluster_name    = aws_eks_cluster.plivo-cluster.name
  node_group_name = "general-nodes"
  node_role_arn   = module.policy.plivo-cluster-nodegroup-role
  subnet_ids = [
    module.network.subnet-1,
    module.network.subnet-2,
    module.network.subnet-3
  ]

  capacity_type  = "ON_DEMAND"
  instance_types = ["t3a.micro"]

  scaling_config {
    desired_size = var.nodes
    max_size     = var.max_nodes
    min_size     = 0
  }

  update_config {
    max_unavailable = 1
  }

  labels = {
    role = "general"
  }
  depends_on = [ module.policy.plivo-cluster-nodegroup-role, module.network.subnet-2 ]
}