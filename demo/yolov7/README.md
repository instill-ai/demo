# 🔥 YOLOv7 demo

This demo is to showcase the official [YOLOv7](https://github.com/WongKinYiu/yolov7) pre-trained model deployed via [VDP](https://github.com/instill-ai/vdp).

## How to run the demo
Run the following command
```bash
# Install dependencies
$ pip install -r requirements.txt

# Run the demo
#   --demo-url=< demo URL >
#   --pipeline-backend-base-url=< pipeline backend base URL >
#   --yolov4=< YOLOv4 pipeline resource name >
#   --yolov7=< YOLOv7 pipeline resource name >
$ streamlit run main.py -- --demo-url=https://demo.instill.tech/yolov4-vs-yolov7 --pipeline-backend-base-url=https://demo.instill.tech --yolov4=pipelines/yolov4 --yolov7=pipelines/yolov7
```
Now go to `http://localhost:8501/` 🎉