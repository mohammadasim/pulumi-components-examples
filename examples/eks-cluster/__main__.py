"""An AWS Python Pulumi program"""

import pulumi
from pulumi_components.aws.components.eks import EksCluster
from pulumi_components.aws.components.vpc import Vpc, VpcSubnetArgs
from pulumi_components.aws.utils import register_tags

from utils import create_iam_role

register_tags()
conf = pulumi.Config()
vpc_conf = conf.get_object("vpc")
env = pulumi.get_stack().split(".")[1]

public_subnets = [
    VpcSubnetArgs(**subnet) for subnet in vpc_conf.get("public_subnets")
]  # noqa E501
private_subnets = [
    VpcSubnetArgs(**subnet) for subnet in vpc_conf.get("private_subnets")
]  # noqa E501

# Create VPC
vpc = Vpc(
    f"{env}-vpc",
    vpc_conf.get("vpc_cidr"),
    public_subnets,
    private_subnets,
    ha_nat=False,
)

# Create an IAM role for EKS cluster administrator
admin_role = create_iam_role(
    "eksClusterRole",
    "Amazon EKS - Cluster role",
    "eks.amazonaws.com",
    managed_policies_arn=["arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"],
)

# Crate eks cluster
cluster = EksCluster(
    f"{env}-eks-cluster",
    admin_role.arn,
    vpc.private_subnet_ids,
    "1.24",
)
# Export the name of the bucket
pulumi.export("vpc_id", vpc.vpc.id)
pulumi.export("eks_cluster", cluster)
