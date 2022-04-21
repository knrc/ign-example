"""An AWS Python Pulumi program"""

import os
import pulumi
import pulumi_aws as aws


def read_ign_file(file_name: str):
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, f'ign_files/{file_name}')

    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')
        print(data)
    return data

size = "t2.micro"
ami = aws.ec2.get_ami(
    most_recent="true",
    owners=["125523088429"],
    filters=[{"name": "name", "values": ["fedora-coreos-35.20220327.3.0-x86_64"]}],
)
resource_prefix = pulumi.Config("resource").require("prefix")
group = aws.ec2.SecurityGroup(
    f"{resource_prefix}-sg",
    name=f"{resource_prefix}-test security group",
    description="Enable HTTP access",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            description="SSH",
            from_port=22,
            to_port=22,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"],
        ),
        aws.ec2.SecurityGroupIngressArgs(
            description="HTTP",
            from_port=80,
            to_port=80,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"],
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            description="enable egress to open to all",
            protocol=-1,
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
        ),
    ],
    tags={"Name": f"{resource_prefix}-ec2"},
)

server = aws.ec2.Instance(
    f"{resource_prefix}-ec2",
    instance_type=size,
    vpc_security_group_ids=[group.id],  # reference security group from above
    ami=ami.id,
    key_name="zpu-key-pair",
    user_data=read_ign_file("hello.ign"),
    tags={"Name": f"{resource_prefix}-ec2"},
)

pulumi.export("publicIp", server.public_ip)
pulumi.export("publicHostName", server.public_dns)
