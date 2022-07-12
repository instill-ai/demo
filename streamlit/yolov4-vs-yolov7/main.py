import argparse
import requests
import json
import cv2
import urllib
import numpy as np
import streamlit as st
from types import SimpleNamespace
from typing import List, Tuple
from urllib.error import HTTPError

from utils import draw_detection, gen_detection_table


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
        json: response json object
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
    for v in r.output[0].detection_outputs[0].bounding_box_objects:
        boxes_ltwh.append((
            v.bounding_box.left,
            v.bounding_box.top,
            v.bounding_box.width,
            v.bounding_box.height))
        categories.append(v.category)
        scores.append(v.score)

    return True, resp.json(), boxes_ltwh, categories, scores


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--demo-url', type=str,
                        default='https://demo.instill.tech/yolov4-vs-yolov7', help='demo URL')
    parser.add_argument('--pipeline-backend-base-url', type=str,
                        default='http://localhost:8081', help='pipeline backend base URL')
    parser.add_argument('--yolov4', type=str,
                        default='pipelines/yolov4', help='YOLOv4 pipeline resource name on VDP')
    parser.add_argument('--yolov7', type=str,
                        default='pipelines/yolov7', help='YOLOv7 pipeline resource name on VDP')
    opt = parser.parse_args()
    print(opt)

    st.set_page_config(page_title="VDP - YOLOv4 vs. YOLOv7",
                       page_icon="https://www.instill.tech/favicon-32x32.png", layout="centered", initial_sidebar_state="auto")

    pipeline_backend_base_url = opt.pipeline_backend_base_url + "/v1alpha"

    st.image("https://raw.githubusercontent.com/instill-ai/.github/main/img/vdp.svg")

    f"""

    # YOLOv4 vs. YOLOv7

    [![Twitter](https://img.shields.io/badge/Twitter-%231DA1F2.svg?style=for-the-badge&logo=Twitter&logoColor=white)](https://twitter.com/intent/tweet?hashtags=%2Cvdp%2Cyolov4%2Cyolov7%2Cstreamlit&original_referer=http%3A%2F%2Flocalhost%3A8501%2F&ref_src=twsrc%5Etfw%7Ctwcamp%5Ebuttonembed%7Ctwterm%5Ehashtag%7Ctwgr%5EYOLOv7&text=%F0%9F%94%A5%F0%9F%94%A5%F0%9F%94%A5%20Try%20out%20VDP%20%2B%20YOLOv7%20demo&url={opt.demo_url})
    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?style=for-the-badge&logo=Facebook&logoColor=white)](https://www.facebook.com/sharer/sharer.php?kid_directed_site=0&sdk=joey&u={opt.demo_url}&display=popup&ref=plugin&src=share_button)
    [![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/sharing/share-offsite/?url={opt.demo_url})

    [Visual Data Preparation (VDP)](https://github.com/instill-ai/vdp) is an open-source visual data ETL tool to streamline the end-to-end visual data processing pipeline

    - 🚀 The fastest way to build end-to-end visual data pipelines
    - 🖱️ One-click import & deploy ML/DL models
    - 🤠 Build for every Vision AI and Data practitioner

    Give us a ⭐ on [![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/instill-ai/vdp) and join our [![Discord](https://img.shields.io/badge/Community-%237289DA.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/sevxWsqpGh)

    #### We are offering **FREE** fully-managed VDP on Instill Cloud
    If you are interested in sharing with the world what your models are capable of, please [sign up the form](https://www.instill.tech/get-access) and we will reach out to you. Seats are limited - first come , first served.

    # Demo

    To spice things up, we use open-source [VDP](https://github.com/instill-ai/vdp) to import the official [YOLOv4](https://github.com/AlexeyAB/darknet) and [YOLOv7](https://github.com/WongKinYiu/yolov7) models pre-trained with only [MS-COCO](https://cocodataset.org) dataset. VDP instantly gives us the endpoints to perform inference:
    1. https://demo.instill.tech/v1alpha/pipelines/yolov4:trigger        
    2. https://demo.instill.tech/v1alpha/pipelines/yolov7:trigger        
        
    Let's trigger two pipelines with an input image each:
    
    """

    vdp_markdown = """
    # What's cool about VDP?

    A VDP pipeline unlocks the value of unstructured visual data:

    1. **Extract** unstructured visual data from pre-built data sources such as cloud/on-prem storage, or IoT devices

    2. **Transform** it into analysable structured data by Vision AI models

    3. **Load** the transformed data into warehouses, applications, or other destinations

    With the help of the VDP pipeline, you can start manipulating the structured data like below in the destination using the tooling in modern data stack.
    """

    image_url = st.text_input(
        label="Feed me with an image URL and press ENTER", value="https://artifacts.instill.tech/dog.jpg")

    try:
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

        """
        #### Results

        Spot any difference?
        """

        col1, col2 = st.columns(2)

        success1, resp1, boxes_ltwh1, categories1, scores1 = trigger_yolo_pipeline_w_remote_image(
            pipeline_backend_base_url, opt.yolov4, image_url)

        success2, resp2, boxes_ltwh2, categories2, scores2 = trigger_yolo_pipeline_w_remote_image(
            pipeline_backend_base_url, opt.yolov7, image_url)

        if success1:
            # Show image overlaid with detection results
            img_draw1 = draw_detection(img, boxes_ltwh1, categories1, scores1)
            col1.image(
                img_draw1, use_column_width=True,
                caption=f"YOLOv4")
        else:
            col1.error("YOLOv4 inference error")

        if success2:
            # Show image overlaid with detection results
            img_draw2 = draw_detection(img, boxes_ltwh2, categories2, scores2)
            col2.image(
                img_draw2, use_column_width=True,
                caption=f"YOLOv7")
        else:
            col2.error("YOLOv7 inference error")

        # Show request
        code = f"""curl -X POST '{pipeline_backend_base_url}/pipelines/<pipeline-id>:trigger' \
        --header 'Content-Type: application/json' \
        --data-raw '{{
            "inputs": [
                {{
                    "image_url": "{image_url}"
                }}
            ]
        }}' 
        """
        with st.expander(f"cURL"):
            st.code(code, language="bash")

        col1, col2 = st.columns(2)
        if success1:
            # Show response
            with col1.expander(f"POST /pipelines/{opt.yolov4}:trigger response"):
                st.json(resp1)

        if success2:
            # Show response
            with col2.expander(f"POST /pipelines/{opt.yolov7}:trigger response"):
                st.json(resp2)

        st.markdown(vdp_markdown)

        col1, col2 = st.columns(2)
        if success1:
            _, df1 = gen_detection_table(
                boxes_ltwh1, categories1, scores1)
            if len(df1):
                col1.dataframe(df1.style.highlight_between(
                    subset='Score', left=0.5, right=1.0))
            else:
                col1.dataframe(df1)

        if success2:
            _, df2 = gen_detection_table(
                boxes_ltwh2, categories2, scores2)
            if len(df2):
                col2.dataframe(df2.style.highlight_between(
                    subset='Score', left=0.5, right=1.0))
            else:
                col2.dataframe(df2)

        st.caption("Highlight detections with score >= 0.5")

    except (ValueError, HTTPError) as err:
        st.error("Can't read the image")
        st.markdown(vdp_markdown)
