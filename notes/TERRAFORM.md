__WARNING:__ This is a work in progress. The `scripts/ses-config/main.tf` script was not used to create the resources in
the cloud. The resources were created manually. First run of this script should be done with caution.

# Variables

The project variables are in:

- `prod.tfvars`

The `prod.tfvars` file is used for the `prod` workspace.

These files are added to the `.gitignore` file so that they are not committed to the repository. There is a
`tfvars.example` file that can be copied to create the `prod.tfvars` file. The `tfvars.example` file contains the
variables that are needed for the project.

# New Machine Setup

```shell
brew install tfenv
#tfenv install latest
tfenv install 1.7.2
```

# Entering Project

After changing into a directory with a `.terraform-version` file, you can set the version with:

```shell
tfenv use
```

... or in .zshrc add this and when you `cd` into this directory it will fix the version for you:

```shell
tfenv_auto() {
    if [[ -f ".terraform-version" ]]; then
        tfenv use
    fi
}
autoload -U add-zsh-hook
add-zsh-hook chpwd tfenv_auto
```

# New Project Setup

The environment was created by running the following commands:

```shell
terraform version
echo "1.7.2" > .terraform-version
tfenv use 1.7.2
terraform init
```

# Adding a new workspace

To create the `stage` workspace (if you wanted to create it) you would run the following command:

```shell
terraform workspace new stage
```

Only the `prod` workspace is currently being used.

# Switching to a different workspace

Currently available workspaces:

- `default` (should be empty)
- `prod`

```shell
terraform workspace select prod
```

# Execution Plan

To create the execution plan and see what the final variables will be, run the following command:

```shell
terraform workspace select prod 
terraform plan -out=prod.tfplan -var-file=prod.tfvars
```

The output will show the variables that will be used in the plan. The plan will be saved to the `prod.tfplan` file.

__NOTE:__ The `prod.tfplan` file is not committed to the repository.

# Checking the Plan

To see the plan that was created, run the following command:

```shell
terraform show prod.tfplan
```

# Execution

WARNING: This will create and modify the resources in the cloud.

```shell
terraform apply prod.tfplan
```

# Marking as good

To mark a resource as good, run the following command:

```shell
terraform untaint aws_instance.copilot_prod_instance
```
