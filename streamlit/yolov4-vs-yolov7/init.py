import typing
from typing import Final

import requests

###############################################################################
# VDP backends
###############################################################################

# TODO: replace with future api-gateway
ver: Final[str] = "v1alpha"
backend: typing.Dict[str, str] = {
    "pipeline": "localhost:18081",
    "connector": "localhost:18082",
    "model": "localhost:18083",
}

###############################################################################
# Source connector
###############################################################################

print("\nCreate a source connector:")
print()
src_conn_id = "source-http"
src_conn = requests.get(
    f'http://{backend["connector"]}/{ver}/source-connectors/{src_conn_id}')
if src_conn.status_code == 404:
    src_conn = requests.post(f'http://{backend["connector"]}/{ver}/source-connectors', json={
        "id": src_conn_id,
        "source_connector_definition": "source-connector-definitions/source-http",
        "connector": {
            "configuration": {}
        },
    })

print(src_conn.json())
print()

###############################################################################
# Destination connector
###############################################################################

print("Create a destination connector:")
print()
dst_conn_id = "destination-http"
dst_conn = requests.get(
    f'http://{backend["connector"]}/{ver}/destination-connectors/{dst_conn_id}')
if dst_conn.status_code == 404:
    dst_conn = requests.post(f'http://{backend["connector"]}/{ver}/destination-connectors', json={
        "id": dst_conn_id,
        "destination_connector_definition": "destination-connector-definitions/destination-http",
        "connector": {
            "configuration": {}
        },
    })

print(dst_conn.json())
print()

###############################################################################
# Model
###############################################################################

print("Create a YOLOv4 model:")
print()
model_id = "yolov4"
model = requests.get(
    f'http://{backend["model"]}/{ver}/models/{model_id}')
if model.status_code == 404:
    model = requests.post(f'http://{backend["model"]}/{ver}/models', json={
        "id": model_id,
        "model_definition": "model-definitions/github",
        "description": "YOLOv4 model imported from GitHub",
        "configuration": {
            "repository": "instill-ai/model-yolov4"
        },
    })

print(model.json())
print()

print("Deploy a YOLOv4 model instance:")
print()
deploy_model_inst = requests.post(
    f'http://{backend["model"]}/{ver}/models/yolov4/instances/v1.0-gpu:deploy')

print(deploy_model_inst.json())
print()

print("Create a YOLOv7 model:")
print()
model_id = "yolov7"
model = requests.get(
    f'http://{backend["model"]}/{ver}/models/{model_id}')
if model.status_code == 404:
    model = requests.post(f'http://{backend["model"]}/{ver}/models', json={
        "id": model_id,
        "model_definition": "model-definitions/github",
        "description": "YOLOv7 model imported from GitHub",
        "configuration": {
            "repository": "instill-ai/model-yolov7"
        },
    })

print(model.json())
print()

print("Deploy a YOLOv7 model instance:")
print()
deploy_model_inst = requests.post(
    f'http://{backend["model"]}/{ver}/models/yolov7/instances/v1.0-gpu:deploy')

print(deploy_model_inst.json())
print()

###############################################################################
# Pipeline
###############################################################################

print("Create pipelines:")
print()
pipeline_id: typing.Dict[str, str] = {
    "yolov4": "yolov4",
    "yolov7": "yolov7",
}

pipeline = requests.get(
    f'http://{backend["pipeline"]}/{ver}/pipelines/{pipeline_id["yolov4"]}')
if pipeline.status_code == 404:
    pipeline = requests.post(f'http://{backend["pipeline"]}/{ver}/pipelines', json={
        "id": pipeline_id["yolov4"],
        "description": "A single model sync pipeline with YOLOv4",
        "recipe": {
            "source": "source-connectors/source-http",
            "model_instances": ["models/yolov4/instances/v1.0-gpu"],
            "destination": f'destination-connectors/destination-http'
        }
    })

print(pipeline.json())
print()

pipeline = requests.get(
    f'http://{backend["pipeline"]}/{ver}/pipelines/{pipeline_id["yolov7"]}')
if pipeline.status_code == 404:
    pipeline = requests.post(f'http://{backend["pipeline"]}/{ver}/pipelines', json={
        "id": pipeline_id["yolov7"],
        "description": "A single model sync pipeline with YOLOv7",
        "recipe": {
            "source": "source-connectors/source-http",
            "model_instances": ["models/yolov7/instances/v1.0-gpu"],
            "destination": f'destination-connectors/destination-http'
        }
    })

print(pipeline.json())
print()
