RAWVERSION = $(filter-out __version__ = , $(shell grep __version__ spectre/__init__.py))
VERSION = $(strip $(shell echo $(RAWVERSION)))

PACKAGE = spectre
FULLPACKAGE = $(PACKAGE)-$(VERSION).tar.gz
SPECFILE = $(PACKAGE).spec
ARCH = $(shell arch)

DOCKER_REGISTRY = 467892444047.dkr.ecr.us-west-2.amazonaws.com/caltech-imss-ads

#======================================================================

aws-login:
	@$(shell aws ecr get-login --region us-west-2 --no-include-email)

# needed because aws/codebuild/docker:1.12.1 is Ubuntu 14.04 with an old version of awscli
aws-login-old:
	@$(shell aws ecr get-login --region us-west-2)

clean:
	rm -rf *.tar.gz dist *.egg-info *.rpm
	find . -name "*.pyc" -exec rm '{}' ';'

version:
	@echo $(VERSION)

image_name:
	@echo ${DOCKER_REGISTRY}/${PACKAGE}:${VERSION}

dist: clean
	@python2.6 setup.py sdist

build:
	docker build -t ${PACKAGE}:${VERSION} .
	docker tag ${PACKAGE}:${VERSION} ${PACKAGE}:latest

force-build: aws-login
	docker build --no-cache -t ${PACKAGE}:${VERSION} .
	docker tag ${PACKAGE}:${VERSION} ${PACKAGE}:latest

codebuild: aws-login-old
	bin/pre-get-dependencies.sh requirements.Docker.txt && mv requirements.Docker.txt.new requirements.Docker.txt
	docker build -t ${PACKAGE}:${VERSION} .
	docker tag ${PACKAGE}:${VERSION} ${PACKAGE}:latest

tag:
	docker tag ${PACKAGE}:${VERSION} ${DOCKER_REGISTRY}/${PACKAGE}:${VERSION}
	docker tag ${PACKAGE}:latest ${DOCKER_REGISTRY}/${PACKAGE}:latest

push: tag
	docker push ${DOCKER_REGISTRY}/${PACKAGE}

dev: devup

down: devdown

devup:
	docker-compose -f docker-compose.yml up -d

devdown:
	docker-compose down

logall:
	docker-compose logs -f

log:
	docker logs -f spectre

exec:
	docker exec -it spectre /bin/bash

docker-clean:
	docker stop $(shell docker ps -a -q)
	docker rm $(shell docker ps -a -q)

docker-destroy-db:
	rm -Rf sql/docker/mysql-data/

docker-destroy: docker-clean docker-destroy-db
	docker rmi -f $(shell docker images -q | uniq)
	docker image prune -f; docker volume prune -f; docker container prune -f

deploy-test: build push
	deploy update spectre-test

deploy-prod: build push
	deploy update spectre-prod

pipeline-create:
	aws codebuild create-project --cli-input-json file://codepipeline/codebuild-spectre-docker-build.json
	aws codebuild create-project --cli-input-json file://codepipeline/codebuild-spectre-test-deploy.json
	aws codebuild create-project --cli-input-json file://codepipeline/codebuild-spectre-prod-deploy.json
	aws codepipeline create-pipeline --cli-input-json file://codepipeline/codepipeline-spectre-test.json
	aws codepipeline create-pipeline --cli-input-json file://codepipeline/codepipeline-spectre-prod.json

pipeline-update-projects:
	aws codebuild update-project --cli-input-json file://codepipeline/codebuild-spectre-docker-build.json
	aws codebuild update-project --cli-input-json file://codepipeline/codebuild-spectre-test-deploy.json
	aws codebuild update-project --cli-input-json file://codepipeline/codebuild-spectre-prod-deploy.json

pipeline-update: pipeline-update-projects
	aws codepipeline update-pipeline --cli-input-json file://codepipeline/codepipeline-spectre-test.json
	aws codepipeline update-pipeline --cli-input-json file://codepipeline/codepipeline-spectre-prod.json

deploy-config-test:
	@deploy config show spectre-test --to-env-file > my-test-env-file.bak
	@test -f my-test-env-file && deploy --env_file=my-test-env-file config write spectre-test || echo 'Environment file "my-test-env-file" not found!'

deploy-config-prod:
	@deploy config show spectre-prod --to-env-file > my-prod-env-file.bak
	@test -f my-prod-env-file && deploy --env_file=my-prod-env-file config write spectre-prod || echo 'Environment file "my-prod-env-file" not found!'

deploy-config-test-restore:
	@cp my-test-env-file.bak my-test-env-file && make deploy-config-test

deploy-config-prod-restore:
	@cp my-prod-env-file.bak my-prod-env-file && make deploy-config-prod


.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs