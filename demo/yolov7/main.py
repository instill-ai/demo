import argparse
import requests
import json
import cv2
import urllib
import numpy as np
import streamlit as st
from types import SimpleNamespace
from typing import List, Tuple

from utils import draw_detection


def test_yolo_w_remote_image(model_backend_base_url: str, model_instance_name: str, image_url: str) -> Tuple[bool, List[Tuple[float]], List[str], List[float]]:
    """ Test a detection model instance (e.g., YOLOv7) with remote image URL

    Args:
        model_backend_base_url (string): VDP model backend base URL
        model_instance_name (string): model instance resource name in the format `models/{model-id}/instances/{instance-id}`
        image_url (string): remote image URL, e.g., `https://artifacts.instill.tech/dog.jpg`

    Returns: a tuple of
        bool: a flag to indicate whether the response is successful
        List[Tuple[float]]: a list of detected bounding boxes in the format of (top, left, width, height)
        List[str]: a list of category labels, each of which corresponds to a detected bounding box. The length of this list must be the same as the detected bounding boxes.
        List[float]]: a list of scores, each of which corresponds to a detected bounding box. The length of this list must be the same as the detected bounding boxes.

    """
    body = {
        "inputs": [
            {
                'image_url': image_url
            }
        ]
    }
    resp = requests.post(
        "{}/{}:test".format(model_backend_base_url, model_instance_name), json=body)

    if resp.status_code != 200:
        return False, [], [], []

    # Parse JSON into an object with attributes corresponding to dict keys.
    r = json.loads(resp.text, object_hook=lambda d: SimpleNamespace(**d))

    boxes_ltwh = []
    categories = []
    scores = []
    for v in r.output.detection_outputs[0].bounding_box_objects:
        boxes_ltwh.append((
            v.bounding_box.left,
            v.bounding_box.top,
            v.bounding_box.width,
            v.bounding_box.height))
        categories.append(v.category)
        scores.append(v.score)
    return True, boxes_ltwh, categories, scores


def is_exist_pipeline(pipeline_backend_base_url, pipeline_name) -> bool:
    """ Check whether a pipeline exists

    Args:
        pipeline_backend_base_url (string): VDP pipeline backend base URL
        pipeline_name (string): pipeline resource name in the format `pipelines/{pipeline-id}`

    Returns: a tuple of
        bool: a flag to indicate whether the pipeline exists
    """
    resp = requests.get(
        "{}/{}".format(pipeline_backend_base_url, pipeline_name))
    if resp.status_code != 200:
        return False
    else:
        return True


def trigger_yolo_pipeline_w_remote_image(pipeline_backend_base_url: str, pipeline_name: str, image_url: str):
    """ Test a pipeline formatted with a detection model instance (e.g., YOLOv7) using remote image URL

    Args:
        pipeline_backend_base_url (string): VDP pipeline backend base URL
        pipeline_name (string): pipeline resource name in the format `pipelines/{pipeline-id}`
        image_url (string): remote image URL, e.g., `https://artifacts.instill.tech/dog.jpg`

    Returns: a tuple of
        bool: a flag to indicate whether the response is successful
        List[Tuple[float]]: a list of detected bounding boxes in the format of (top, left, width, height)
        List[str]: a list of category labels, each of which corresponds to a detected bounding box. The length of this list must be the same as the detected bounding boxes.
        List[float]]: a list of scores, each of which corresponds to a detected bounding box. The length of this list must be the same as the detected bounding boxes.

    """
    body = {
        "inputs": [
            {
                'image_url': image_url
            }
        ]
    }

    resp = requests.post(
        "{}/{}:trigger".format(pipeline_backend_base_url, pipeline_name), json=body)

    if resp.status_code != 200:
        return False, [], [], []

    # Parse JSON into an object with attributes corresponding to dict keys.
    r = json.loads(resp.text, object_hook=lambda d: SimpleNamespace(**d))

    boxes_ltwh = []
    categories = []
    scores = []
    for v in r.output.detection_outputs[0].bounding_box_objects:
        boxes_ltwh.append((
            v.bounding_box.left,
            v.bounding_box.top,
            v.bounding_box.width,
            v.bounding_box.height))
        categories.append(v.category)
        scores.append(v.score)

    return True, boxes_ltwh, categories, scores


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-backend-base-url', type=str,
                        default='http://localhost:8083/v1alpha', help='model backend base URL')
    parser.add_argument('--yolov4', type=str,
                        default='models/yolov4/instances/v1.0-cpu', help='YOLOv4 model instance resource name on VDP')
    parser.add_argument('--yolov7', type=str,
                        default='models/yolov7/instances/v1.0-cpu', help='YOLOv4 model instance resource name on VDP')
    opt = parser.parse_args()
    print(opt)

    """
    # 🔥🔥🔥 [VDP + YOLOv7] What's in the 🖼️?

    [Visual Data Preparation (VDP)](https://github.com/instill-ai/vdp) is an open-source visual data ETL tool to streamline the end-to-end visual data processing pipeline

    - 🚀 The fastest way to build end-to-end visual data pipelines
    - 🖱️ One-click import & deploy ML/DL models
    - 🤠 Build for every Vision AI and Data practitioner

    """
    st.markdown(
        '<span style="color:DarkOrchid">**Give us a ⭐ on [GitHub](https://github.com/instill-ai/vdp) and join our [community](https://discord.gg/sevxWsqpGh)!**</span>', True)

    """
    #### Free model hosting with Instill Cloud
    🚀 We offer freemium for hosting models in Instill Cloud. [Sign up alpha user form](https://www.instill.tech/get-access) now and we will contact you to onboard your models.
    
    ## Demo

    We use open-source [**VDP**](https://github.com/instill-ai/vdp) to deploy the official [**YOLOv7**](https://github.com/WongKinYiu/yolov7) pre-trained model for the demo.
    """
    image_url = st.text_input(
        label="Feed me with an image URL and press ENTER", value="https://artifacts.instill.tech/dog.jpg")

    req = urllib.request.Request(
        image_url, headers={'User-Agent': "XYZ/3.0"})
    con = urllib.request.urlopen(req, timeout=10)
    arr = np.asarray(bytearray(con.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # Visualization
    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
    col2.image(
        img,
        use_column_width=True,
        caption=f"Image source: {image_url}")

    st.markdown("#### YOLOv4 vs. YOLOv7 detection")
    col1, col2 = st.columns(2)

    success1, boxes_ltwh1, categories1, scores1 = test_yolo_w_remote_image(
        opt.model_backend_base_url, opt.yolov4, image_url)

    success2, boxes_ltwh2, categories2, scores2 = test_yolo_w_remote_image(
        opt.model_backend_base_url, opt.yolov7, image_url)

    if success1:
        img_draw1 = draw_detection(img, boxes_ltwh1, categories1, scores1)
        col1.image(
            img_draw1, use_column_width=True,
            caption=f"YOLOv4")
    else:
        col1.error("YOLOv4 inference error")

    if success2:
        img_draw2 = draw_detection(img, boxes_ltwh2, categories2, scores2)
        col2.image(
            img_draw2, use_column_width=True,
            caption=f"YOLOv7")
    else:
        col2.error("YOLOv7 inference error")
