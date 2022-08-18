.DEFAULT_GOAL:=help

TEMPORAL := temporal temporal_admin_tools temporal_ui

#============================================================================

# load environment variables
include .env
export

TRITONSERVER_IMAGE_TAG := $(if $(filter arm64,$(shell uname -m)),instill/tritonserver:${TRITON_SERVER_VERSION}-py3-cpu-arm64,nvcr.io/nvidia/tritonserver:${TRITON_SERVER_VERSION}-py3)
TRITONCONDAENV_IMAGE_TAG := $(if $(filter arm64,$(shell uname -sm)),instill/triton-conda-env:${TRITON_CONDA_ENV_VERSION}-m1,instill/triton-conda-env:${TRITON_CONDA_ENV_VERSION}-cpu)
REDIS_IMAGE_TAG := $(if $(filter arm64,$(shell uname -m)),arm64v8/redis:${REDIS_VERSION}-alpine,amd64/redis:${REDIS_VERSION}-alpine)

NVIDIA_SMI := $(shell nvidia-smi 2>/dev/null 1>&2; echo $$?)
ifeq ($(NVIDIA_SMI),0)
	TRITONSERVER_RUNTIME := nvidia
	TRITONCONDAENV_IMAGE_TAG := instill/triton-conda-env:${TRITON_CONDA_ENV_VERSION}-gpu
endif

#============================================================================

.PHONY: all
all:			## Launch all services with their up-to-date release version
	@docker inspect --type=image ${TRITONSERVER_IMAGE_TAG} >/dev/null 2>&1 || printf "\033[1;33mWARNING:\033[0m This may take a while due to the enormous size of the Triton server image, but the image pulling process should be just a one-time effort.\n" && sleep 5
	@docker-compose up -d
	@python3 streamlit/yolov4-vs-yolov7/init.py

.PHONY: logs
logs:			## Tail all logs with -n 10
	@docker-compose logs --follow --tail=10

.PHONY: pull
pull:			## Pull all service images
	@docker inspect --type=image ${TRITONSERVER_IMAGE_TAG} >/dev/null 2>&1 || printf "\033[1;33mWARNING:\033[0m This may take a while due to the enormous size of the Triton server image, but the image pulling process should be just a one-time effort.\n" && sleep 5
	@docker-compose pull

.PHONY: stop
stop:			## Stop all components
	@docker-compose stop

.PHONY: start
start:			## Start all stopped services
	@docker-compose start

.PHONY: restart
restart:		## Restart all services
	@docker-compose restart

.PHONY: rm
rm:				## Remove all stopped service containers
	@docker-compose rm -f

.PHONY: down
down:			## Stop all services and remove all service containers and volumes
	@docker-compose down -v

.PHONY: images
images:			## List all container images
	@docker-compose images

.PHONY: ps
ps:				## List all service containers
	@docker-compose ps

.PHONY: top
top:			## Display all running service processes
	@docker-compose top

.PHONY: doc
doc:			## Run Redoc for OpenAPI spec at http://localhost:3001
	@docker-compose up -d redoc_openapi

config:				## Output the composed KrakenD configuration for debugging
	@bash krakend/envsubst.sh
	@FC_ENABLE=1 FC_SETTINGS="krakend/settings" FC_PARTIALS="krakend/partials" FC_TEMPLATES="krakend/templates" FC_OUT="krakend/out.json" krakend check -d -c krakend/base.json
	@jq . krakend/out.json > krakend.json
	@rm krakend/out.json && rm -rf krakend/settings
.PHONY: config

.PHONY: help
help:       	## Show this help
	@echo "\nMake Application using Docker-Compose files."
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m (default: help)\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
