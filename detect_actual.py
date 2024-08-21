from ultralytics import YOLO
import cv2
from ultralytics.utils.plotting import Annotator
from cvzone.SerialModule import SerialObject
import time

# Initialize YOLOv8n model
model = YOLO('yolov8n.pt')

# Define classes for vehicle detection
vehicle_classes = ['bicycle', 'car', 'motorcycle', 'bus', 'truck']

# Initialize Arduino communication
arduino = SerialObject("COM5")

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    start_time = time.time()
    detected = set()
    while (time.time()-start_time)<=10:
        _, img = cap.read()

        # Perform inference with YOLOv8n
        results = model.predict(img)

        for r in results:
            annotator = Annotator(img)

            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                c = int(box.cls)  # get class ID
                label = model.names[c]  # get class label

                # Draw bounding box and label on the image
                annotator.box_label(b, label)

                detected.add(label)
                 
        img = annotator.result()
        cv2.imshow('YOLO V8 Detection', img)

        # Exit loop if 'e' is pressed
        key = cv2.waitKey(1)
        if key == ord('e'):
            arduino.sendData([2])
            break

    if key == ord('e'):
        arduino.sendData([2])
        break
    
    while (time.time()-start_time)>10 and (time.time()-start_time)<=20:
        _, img = cap.read()
        cv2.imshow('YOLO V8 Detection', img)
                
        if len(detected) > 1:
            arduino.sendData([0])  # Send '0' to Arduino
            if detected.issubset(vehicle_classes):
                print("Only one vehicle at a time!") 
            else:
                print("Not a vehicle, entry not allowed!")

        elif len(detected) == 1:
            if detected.issubset(vehicle_classes):
                arduino.sendData([1])  # Send '1' to Arduino
                print(f"Vehicle detected: {detected.pop()}, entry allowed.")
            else:
                arduino.sendData([0]) # Send '0' to Arduino
                print("Not a vehicle, entry not allowed!")
        
        # Exit loop if 'e' is pressed
        key = cv2.waitKey(1)
        if key == ord('e'):
            arduino.sendData([2])
            break
        
    if key == ord('e'):
        arduino.sendData([2])
        break
    
# Release webcam and close all windows
cap.release()
cv2.destroyAllWindows()