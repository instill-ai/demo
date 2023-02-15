import typing

import requests
import time

###############################################################################
# VDP backends
###############################################################################

# TODO: replace with future api-gateway
ver = "v1alpha"
backend: typing.Dict[str, str] = {
    "pipeline": "localhost:8080",
    "connector": "localhost:8080",
    "model": "localhost:8080",
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
            "repository": "instill-ai/model-yolov4-dvc"
        },
    })

print(model.json())
print()

time.sleep(5)

print("Deploy a YOLOv4 model instance:")
print()
deploy_model_inst = requests.post(
    f'http://{backend["model"]}/{ver}/models/{model_id}/instances/v1.0-gpu/deploy')

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
            "repository": "instill-ai/model-yolov7-dvc"
        },
    })

print(model.json())
print()

time.sleep(5)

print("Deploy a YOLOv7 model instance:")
print()
deploy_model_inst = requests.post(
    f'http://{backend["model"]}/{ver}/models/{model_id}/instances/v1.0-gpu/deploy')

print(deploy_model_inst.json())
print()

print("Create an Intsance Segmentation model:")
print()
model_id = "instance-segmentation"
model = requests.get(
    f'http://{backend["model"]}/{ver}/models/{model_id}')
if model.status_code == 404:
    model = requests.post(f'http://{backend["model"]}/{ver}/models', json={
        "id": model_id,
        "model_definition": "model-definitions/github",
        "description": "Instance Segmentation model imported from GitHub",
        "configuration": {
            "repository": "instill-ai/model-instance-segmentation-dvc"
        },
    })

print(model.json())
print()

time.sleep(5)

print("Deploy an Instance Segmentation model instance:")
print()
deploy_model_inst = requests.post(
    f'http://{backend["model"]}/{ver}/models/{model_id}/instances/v1.0-gpu/deploy')

print(deploy_model_inst.json())
print()

print("Create an Stomata Instance Segmentation model:")
print()
model_id = "stomata-instance-segmentation"
model = requests.get(
    f'http://{backend["model"]}/{ver}/models/{model_id}')
if model.status_code == 404:
    model = requests.post(f'http://{backend["model"]}/{ver}/models', json={
        "id": model_id,
        "model_definition": "model-definitions/github",
        "description": "Stomata Instance Segmentation model imported from GitHub",
        "configuration": {
            "repository": "instill-ai/model-stomata-instance-segmentation-dvc"
        },
    })

print(model.json())
print()

time.sleep(5)

print("Deploy an Stomata Instance Segmentation model instance:")
print()
deploy_model_inst = requests.post(
    f'http://{backend["model"]}/{ver}/models/{model_id}/instances/v2.0-gpu/deploy')

print(deploy_model_inst.json())
print()

print("Create an OCR model:")
print()
model_id = "ocr"
model = requests.get(
    f'http://{backend["model"]}/{ver}/models/{model_id}')
if model.status_code == 404:
    model = requests.post(f'http://{backend["model"]}/{ver}/models', json={
        "id": model_id,
        "model_definition": "model-definitions/github",
        "description": "OCR model imported from GitHub",
        "configuration": {
            "repository": "instill-ai/model-ocr-dvc"
        },
    })

print(model.json())
print()

time.sleep(5)

print("Deploy an OCR model instance:")
print()
deploy_model_inst = requests.post(
    f'http://{backend["model"]}/{ver}/models/{model_id}/instances/v1.0-gpu/deploy')

print(deploy_model_inst.json())
print()

# print("Create a keypoint model:")
# print()
# model_id = "keypoint"
# model = requests.get(
#     f'http://{backend["model"]}/{ver}/models/{model_id}')
# if model.status_code == 404:
#     model = requests.post(f'http://{backend["model"]}/{ver}/models', json={
#         "id": model_id,
#         "model_definition": "model-definitions/github",
#         "description": "Keypoint model imported from GitHub",
#         "configuration": {
#             "repository": "instill-ai/model-keypoint-detection-dvc"
#         },
#     })

# print(model.json())
# print()

# time.sleep(5)

# print("Deploy a keypoint model instance:")
# print()
# deploy_model_inst = requests.post(
#     f'http://{backend["model"]}/{ver}/models/{model_id}/instances/v1.0-gpu/deploy')

# print(deploy_model_inst.json())
# print()

###############################################################################
# Pipeline
###############################################################################

print("Create pipelines:")
print()
pipeline_id: typing.Dict[str, str] = {
    "yolov4": "yolov4",
    "yolov7": "yolov7",
    "keypoint": "keypoint",
    "ocr": "ocr",
    "instance_segmentation": "instance-segmentation",
    "stomata": "stomata",
}

pipeline = requests.get(
    f'http://{backend["pipeline"]}/{ver}/pipelines/{pipeline_id["yolov4"]}')
if pipeline.status_code == 404:
    pipeline = requests.post(f'http://{backend["pipeline"]}/{ver}/pipelines', json={
        "id": pipeline_id["yolov4"],
        "description": "A single model sync pipeline for YOLOv4 demo",
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
        "description": "A single model sync pipeline for YOLOv7 demo",
        "recipe": {
            "source": "source-connectors/source-http",
            "model_instances": ["models/yolov7/instances/v1.0-gpu"],
            "destination": f'destination-connectors/destination-http'
        }
    })

print(pipeline.json())
print()

pipeline = requests.get(
    f'http://{backend["pipeline"]}/{ver}/pipelines/{pipeline_id["instance_segmentation"]}')
if pipeline.status_code == 404:
    pipeline = requests.post(f'http://{backend["pipeline"]}/{ver}/pipelines', json={
        "id": pipeline_id["instance_segmentation"],
        "description": "A single model sync pipeline for Instance Segmentation demo",
        "recipe": {
            "source": "source-connectors/source-http",
            "model_instances": ["models/instance-segmentation/instances/v1.0-gpu"],
            "destination": f'destination-connectors/destination-http'
        }
    })

print(pipeline.json())
print()

pipeline = requests.get(
    f'http://{backend["pipeline"]}/{ver}/pipelines/{pipeline_id["stomata"]}')
if pipeline.status_code == 404:
    pipeline = requests.post(f'http://{backend["pipeline"]}/{ver}/pipelines', json={
        "id": pipeline_id["stomata"],
        "description": "A single model sync pipeline for Stomata Instance Segmentation demo",
        "recipe": {
            "source": "source-connectors/source-http",
            "model_instances": ["models/stomata-instance-segmentation/instances/v2.0-gpu"],
            "destination": f'destination-connectors/destination-http'
        }
    })

print(pipeline.json())
print()

pipeline = requests.get(
    f'http://{backend["pipeline"]}/{ver}/pipelines/{pipeline_id["ocr"]}')
if pipeline.status_code == 404:
    pipeline = requests.post(f'http://{backend["pipeline"]}/{ver}/pipelines', json={
        "id": pipeline_id["ocr"],
        "description": "A single model sync pipeline for OCR demo",
        "recipe": {
            "source": "source-connectors/source-http",
            "model_instances": ["models/ocr/instances/v1.0-gpu"],
            "destination": f'destination-connectors/destination-http'
        }
    })

print(pipeline.json())
print()

# pipeline = requests.get(
#     f'http://{backend["pipeline"]}/{ver}/pipelines/{pipeline_id["keypoint"]}')
# if pipeline.status_code == 404:
#     pipeline = requests.post(f'http://{backend["pipeline"]}/{ver}/pipelines', json={
#         "id": pipeline_id["keypoint"],
#         "description": "A single model sync pipeline for keypoint demo",
#         "recipe": {
#             "source": "source-connectors/source-http",
#             "model_instances": ["models/keypoint/instances/v1.0-gpu"],
#             "destination": f'destination-connectors/destination-http'
#         }
#     })

# print(pipeline.json())
# print()
