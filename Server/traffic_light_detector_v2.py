import cv2
from keras.models import load_model
import numpy as np


np.set_printoptions(suppress=True)

model = load_model("traffic_lights.h5", compile=False)

def process_traffic_lights(frame):
    orig_frame = cv2.resize(frame, (204, 360))
    frame = orig_frame[10:100, 40:-40]
    frame = cv2.resize(frame, (224, 224))
    
    image = np.asarray(frame, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1
    prediction = model.predict(image)
    index = np.argmax(prediction)

    if ((index == 0 or index == 1) and prediction[0][index] > 0.6):
        return index
    return -1

if __name__ == '__main__':
    cap = cv2.VideoCapture("C:\\Users\\knott\\2024-hack-cupertino-proj\\IMG_0159.MOV")
    while cap.isOpened():
        ret, frame = cap.read()

        light = process_traffic_lights(frame)

        crossingText = "Lost Traffic Light"

        if (light == 1):
            crossingText = "Can cross"
        elif (light == 0):
            crossingText = "Don't cross"


        font = cv2.FONT_HERSHEY_SIMPLEX 
  
        org = (50, 50) 
        
        fontScale = 1
        
        color = (255, 0, 0) 
        
        thickness = 2
        
        frame = cv2.putText(frame, crossingText, org, font,  
                        fontScale, color, thickness, cv2.LINE_AA) 

        cv2.imshow('FRAME', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()