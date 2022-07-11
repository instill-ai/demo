# 🔥 YOLOv7 demo

This demo is to showcase the official [YOLOv7](https://github.com/WongKinYiu/yolov7) pre-trained model deployed via [VDP](https://github.com/instill-ai/vdp).

## How to run the demo
Run the following command
```bash
# Install dependencies
$ pip install -r requirements.txt

# Run the demo
# --model-backend-base-url=< model backend base url >
# --yolov4=< YOLOv4 model instance resource name >
# --yolov7=< YOLOv7 model instance resource name >
$ streamlit run main.py -- --model-backend-base-url=https://demo.instill.tech/v1alpha --yolov4=models/yolov4/instances/v1.0-gpu --yolov7=models/yolov7/instances/v1.0-gpu
```
Now go to `http://localhost:8501/` 🎉