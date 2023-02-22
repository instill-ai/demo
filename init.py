import typing

import requests
import time

###############################################################################
# VDP backends
###############################################################################


# TODO: replace with future api-gateway
ver = "v1alpha"
api_backend = "localhost:8080"


def create_github_model(repository, model_id, description=""):
    print("Create a GitHub model: {} from {}".format(model_id, repository))
    model = requests.get(
        f'http://{api_backend}/{ver}/models/{model_id}')
    if model.status_code == 404:
        model = requests.post(f'http://{api_backend}/{ver}/models', json={
            "id": model_id,
            "model_definition": "model-definitions/github",
            "description": description,
            "configuration": {
                "repository": repository
            },
        })
    else:
        print("Model already exists: ", model_id)
    print(model.json())
    print()


def deploy_model_instance(model_id, model_instance_id):
    print("Deploy a {} model instance: {}".format(model_id, model_instance_id))
    print()
    deploy_model_inst = requests.post(
        f'http://{api_backend}/{ver}/models/{model_id}/instances/{model_instance_id}/deploy')
    print(deploy_model_inst.json())
    print()


def create_sync_http_pipeline(pipeline_id, model_instance_name, description=""):
    print("Create a pipeline: {}".format(pipeline_id))
    pipeline = requests.get(
        f'http://{api_backend}/{ver}/pipelines/{pipeline_id}')
    if pipeline.status_code == 404:
        pipeline = requests.post(f'http://{api_backend}/{ver}/pipelines', json={
            "id": pipeline_id,
            "description": description,
            "recipe": {
                "source": "source-connectors/source-http",
                "model_instances": [model_instance_name],
                "destination": f'destination-connectors/destination-http'
            }
        })
    else:
        print("Pipeline already exists: ", pipeline_id)
    print(pipeline.json())
    print()

###############################################################################
# Source connector
###############################################################################


print("\nCreate a source connector:")
print()
src_conn_id = "source-http"
src_conn = requests.get(
    f'http://{api_backend}/{ver}/source-connectors/{src_conn_id}')
if src_conn.status_code == 404:
    src_conn = requests.post(f'http://{api_backend}/{ver}/source-connectors', json={
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
    f'http://{api_backend}/{ver}/destination-connectors/{dst_conn_id}')
if dst_conn.status_code == 404:
    dst_conn = requests.post(f'http://{api_backend}/{ver}/destination-connectors', json={
        "id": dst_conn_id,
        "destination_connector_definition": "destination-connector-definitions/destination-http",
        "connector": {
            "configuration": {}
        },
    })

print(dst_conn.json())
print()

###############################################################################
# GitHub Model
###############################################################################

print("###################### Create GitHub models and SYNC HTTP pipelines ######################")
print()
github: typing.Dict[str, typing.List[typing.Dict[str, str]]] = {
    "Image Classification": [
        {
            "model_id": "mobilenetv2",
            "repository": "instill-ai/model-mobilenetv2",
            "model_description": "MobileNetV2 model imported from GitHub",
            "model_instance_id": "v1.0-gpu",
            "pipeline_id": "mobilenetv2",
            "pipeline_description": "A single model sync pipeline for Image Classfication demo with MobileNetV2 model"
        }
    ],
    "Object Detection": [
        {
            "model_id": "yolov4",
            "repository": "instill-ai/model-yolov4-dvc",
            "model_description": "YOLOv4 model imported from GitHub",
            "model_instance_id": "v1.0-gpu",
            "pipeline_id": "yolov4",
            "pipeline_description": "A single model sync pipeline for Object Detection demo with YOLOv4 model"
        },
        {
            "model_id": "yolov7",
            "repository": "instill-ai/model-yolov7-dvc",
            "model_description": "YOLOv7 model imported from GitHub",
            "model_instance_id": "v1.0-gpu",
            "pipeline_id": "yolov7",
            "pipeline_description": "A single model sync pipeline for Object Detection demo with YOLOv7 model"
        }
    ],
    "Keypoint Detection": [
        {
            "model_id": "keypoint",
            "repository": "instill-ai/model-keypoint-detection-dvc",
            "model_description": "Detectron2 R-CNN R50-FPN Keypoint model imported from GitHub",
            "model_instance_id": "v1.0-gpu",
            "pipeline_id": "keypoint",
            "pipeline_description": "A single model sync pipeline for Keypoint Detection demo with R-CNN R50-FPN model from Detectron2"
        },
        {
            "model_id": "yolov7-pose",
            "repository": "instill-ai/model-yolov7-pose-dvc",
            "model_description": "YOLOv7 Pose Estimation model imported from GitHub",
            "model_instance_id": "v1.0-gpu",
            "pipeline_id": "yolov7-pose",
            "pipeline_description": "A single model sync pipeline for Keypoint Detection demo with YOLOv7 Pose Estimation model"
        }
    ],
    "OCR": [
        {
            "model_id": "ocr",
            "repository": "instill-ai/model-ocr-dvc",
            "model_description": "PSNet + EasyOCR Optical Character Recognition (OCR) model imported from GitHub",
            "model_instance_id": "v1.0-gpu",
            "pipeline_id": "ocr",
            "pipeline_description": "A single model sync pipeline for Optical Character Recognition (OCR) demo"
        }
    ],
    "Instance Segmentation": [
        {
            "model_id": "instance-segmentation",
            "repository": "instill-ai/model-instance-segmentation-dvc",
            "model_description": "Mask RCNN Instance Segmentation model imported from GitHub",
            "model_instance_id": "v1.0-gpu",
            "pipeline_id": "instance-segmentation",
            "pipeline_description": "A single model sync pipeline for Instance Segmentation demo with Mask RCNN model"
        },
        {
            "model_id": "stomata-instance-segmentation",
            "repository": "instill-ai/model-stomata-instance-segmentation-dvc",
            "model_description": "Stomata Instance Segmentation model imported from GitHub",
            "model_instance_id": "v2.0-gpu",
            "pipeline_id": "stomata",
            "pipeline_description": "A single model sync pipeline for Stomata Instance Segmentation demo with custom trained Mask RCNN model"
        }
    ],
    "Sementic Segmentation": [
        {
            "model_id": "semantic-segmentation",
            "repository": "instill-ai/model-semantic-segmentation-dvc",
            "model_description": "Lite R-ASPP based on MobileNetV3 Semantic Segmentation model imported from GitHub",
            "model_instance_id": "v1.0-gpu",
            "pipeline_id": "semantic-segmentation",
            "pipeline_description": "A single model sync pipeline for Semantic Segmentation demo"
        }
    ],
    "Text to Image": [
        {
            "model_id": "stable-diffusion",
            "repository": "instill-ai/model-diffusion-dvc",
            "model_description": "Stable Diffusion Text to Image model imported from GitHub",
            "model_instance_id": "fp32-gpu",
            "pipeline_id": "stable-diffusion",
            "pipeline_description": "A single model sync pipeline for Text to Image demo with Stable Diffusion model"
        }
    ],
    "Text Generation": [
        {
            "model_id": "gpt2",
            "repository": "instill-ai/model-gpt2-megatron-dvc",
            "model_description": "GPT2 Text Generation model imported from GitHub",
            "model_instance_id": "fp32-345m-4-gpus",
            "pipeline_id": "gpt2",
            "pipeline_description": "A single model sync pipeline for Text Generation demo with GPT2 model"
        }
    ]
}
for task, item_ls in github.items():
    print("###################### {}".format(task))
    print()
    for item in item_ls:
        model_id = item["model_id"]
        model_instance_id = item["model_instance_id"]
        create_github_model(item["repository"], model_id,
                            item["model_description"])
        time.sleep(5)
        deploy_model_instance(model_id, model_instance_id)
        time.sleep(5)
        model_instance_name = f"models/{model_id}/instances/{model_instance_id}"
        create_sync_http_pipeline(
            item["pipeline_id"], model_instance_name, item["pipeline_description"])
