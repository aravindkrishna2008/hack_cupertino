from ultralytics import YOLO
import cv2

model = YOLO("yolov8x.pt")

def process_car_detect(frame, centerLine, centerLineThreshold = 20):
    frame = cv2.resize(frame, (204, 360))
    results = model.predict(frame, conf=0.5)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]
            cx = (b[2] + b[0])/2

            if (abs(cx - centerLine) < centerLineThreshold):
                return 1

    return 0