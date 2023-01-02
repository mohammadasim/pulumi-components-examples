## Pulumi-components examples
Here I am creating some example projects that use the `prima-components` library.
I am using `poetry` to manage the project dependencies.
### How to create a new project
`pulumi new aws-python --name <project-name> --secrets-provider=awskms://1234abcd-12ab-34cd-56ef-1234567890ab?region=<kms-key-region>`
This command will create a new pulumi AWS python project. The above command has the following prerequisites:
* Install `pulumi-cli` on your workstation. Follow [this guide](https://www.pulumi.com/docs/get-started/install/)
* Install `aws-cli` and configure it.
* Create an `s3` bucket and run the command `pulumi login s3://<pulumi-state-bucket-name>`
* Create a `kms` key and grant `encrypt` `decrypt` permissions to the user or IAM role that you are using in this project.
* Run the above cited command.

The above command will take you through some interactive steps and at the end of those steps you will have created a stack for your project.
It will also create a new `venv` for your project. In my case I am using `poetry` and hence I will use
the `venv` created by poetry to run this project.
### How to run the project
To create the resources and apply our changes, you will need to run the command `pulumi up`. After you have checked the changes and are happy with the changes choose the `yes` option.
