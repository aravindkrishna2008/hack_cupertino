from flask import Flask, request, Response
import cv2
import numpy as np
import uuid
import base64
from PIL import Image
from io import StringIO
from flask import jsonify
import json

from flask_cors import CORS

from traffic_light_detector_v2 import process_traffic_lights
from crossing_finder import get_crossing
# from car_detection import process_car_detect

app = Flask(__name__)
CORS(app)

@app.route('/api/process-frame', methods=['POST'])
def process_frame():
    if 'frame' not in request.form:
        return jsonify({"light":"TL Error", "crosswalk":0, "car": 0})
    try:
        base64_data = request.form['frame']

        image_data = base64.b64decode(base64_data.split(',')[1])

        filename = "temp.jpg"

        with open(filename, 'wb') as f:
            f.write(image_data)

        img = cv2.imread(filename)
        cimg = img
        light = (process_traffic_lights(img))

        crossing_visible, img, crossing_line = get_crossing(img)

        lightStatus = "Lost Traffic Light"

        if (light == 1):
            lightStatus = "Can cross"
        elif (light == 0):
            lightStatus = "Don't cross"

        cv2.imwrite("static/out.jpg", img)

        # car = process_car_detect(cimg, crossing_line)

        return jsonify({"light":lightStatus, "crosswalk":crossing_visible, "car": 0})
    except:
        pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=846, debug=True)
