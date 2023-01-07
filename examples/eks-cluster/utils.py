import json
from typing import Optional, Sequence

import pulumi_aws as aws


def create_iam_role(
    role_name: str,
    description: str,
    service: str,
    inline_policies: Optional[Sequence[aws.iam.RoleInlinePolicyArgs]] = [],
    managed_policies_arn: Optional[Sequence[str]] = [],
) -> aws.iam.Role:
    """Creates and returns IAM role with permissions defined
    in the inline managed policies"""
    if not inline_policies and not managed_policies_arn:
        raise ValueError(
            "You must define either an inline policy or managed policy arns"
        )  # noqa E501
    if not service:
        raise ValueError("You must define an aws service for IAM role")
    trust_policy = json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": f"{service}"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }
    )
    role = aws.iam.Role(
        role_name,
        name=role_name,
        description=description,
        assume_role_policy=trust_policy,
        managed_policy_arns=managed_policies_arn,
        inline_policies=inline_policies,
    )
    return role
