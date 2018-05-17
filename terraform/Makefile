config:
	terraform init

pull:
	terraform state pull

plan: config pull
	terraform plan

push:
	@test -e .terraform/terraform.tfstate && terraform state push

force-push:
	aws s3 cp .terraform/terraform.tfstate s3://caltech-terraform-remotestate-file/spectre-terraform-state