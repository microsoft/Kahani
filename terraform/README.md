# Deployment via Terraform

Terraform allows us to describe our infrastructure in code.

1. Create the config file
```terraform
resource_group_name = ""
storage_account_name = ""
container_name = ""
key = ""
```

2. Create the variables file
```
SDAPI_HOST = ""
OPENAI_API_KEY = ""
container_registry = ""
container_registry_username = ""
container_registry_password = ""
```

3. Run the deployment setup
```bash
$ terraform init -backend-config=config.dev.tfbackend
$ terraform plan -out=plan
$ terraform apply "plan"
```