"""An AWS Python Pulumi program"""

import pulumi
from pulumi_components.aws.components.rds import RDSInstance
from pulumi_components.aws.components.vpc import Vpc, VpcSubnetArgs
from pulumi_components.aws.utils import register_tags

# register tags
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
# Create an RDS instance
rds_conf = conf.get_object("rds")
rds_instance = RDSInstance(
    f"{env}-rds-instance",
    rds_conf.get("allocated_storage"),
    rds_conf.get("instance_class"),
    rds_conf.get("engine"),
    rds_conf.get("engine_version"),
    rds_conf.get("family"),
    f"{env}-rds-instance",
    rds_conf.get("username"),
    pulumi.Output.secret(rds_conf.get("password")),
    vpc.vpc.id,
    db_name=rds_conf.get("db_name"),
    ingress_security_group_cidrs=[vpc.vpc.cidr_block],
    subnet_ids=vpc.private_subnet_ids,
)

pulumi.export("vpc_id", vpc.vpc.id)
