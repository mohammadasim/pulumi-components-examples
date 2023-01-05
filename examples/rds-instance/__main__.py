"""An AWS Python Pulumi program"""

import pulumi
from pulumi_components.aws.components.rds import AuroraCluster, RDSInstance
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
# Create Aurora cluster
aurora_conf = conf.get_object("aurora")
aurora_cluster = AuroraCluster(
    f"{env}-aurora-psql-cluster",
    cluster_parameters=[],
    db_parameters=[],
    family=aurora_conf.get("family"),
    engine=aurora_conf.get("engine"),
    engine_version=aurora_conf.get("engine_version"),
    master_password=pulumi.Output.secret(aurora_conf.get("master_password")),
    subnet_ids=vpc.private_subnet_ids,
    vpc_id=vpc.vpc.id,
    availability_zones=["eu-west-1a", "eu-west-1b", "eu-west-1c"],
    instances=aurora_conf.get("instances"),
    ingress_security_group_cidrs=[vpc.vpc.cidr_block],
)
pulumi.export("vpc_id", vpc.vpc.id)
