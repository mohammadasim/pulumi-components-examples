"""An AWS Python Pulumi program"""

import pulumi
from pulumi_components.aws.utils import register_tags
from pulumi_components.aws.components.vpc import Vpc, VpcSubnetArgs


# register tags
register_tags()

conf = pulumi.Config()
vpc_conf = conf.get_object("vpc")
env = pulumi.get_stack().split(".")[1]

public_subnets = [VpcSubnetArgs(**subnet) for subnet in vpc_conf.get("public_subnets")]
private_subnets = [VpcSubnetArgs(**subnet) for subnet in vpc_conf.get("private_subnets")]

# Create VPC
vpc = Vpc(
    f"{env}-vpc",
    vpc_conf.get("vpc_cidr"),
    public_subnets,
    private_subnets,
    ha_nat=False,
)

