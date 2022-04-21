# prerequisite
Please help `Pulumi` (`brew install pulumi`), Python and (awscli)(https://aws.amazon.com/cli/) installed, also after awscli is installed, run the `aws configure` to use your own aws access_key_id and aws_secret_access_key

# How to run
You can create your own Pulumi stack, and update the resources names accordingly, then run the `pulumi up`

# Ignition file 
The repository includes a sample ignition file: `hello.ign`, this ignition file will be included as `user_data` when provision the EC2 instance
