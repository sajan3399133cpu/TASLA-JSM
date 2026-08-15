import asyncio
import json
import cv2
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from ultralytics import YOLO

app = FastAPI()

# YOLOv8 Model Initialization
model = YOLO('yolov8n.pt')

# Distance estimation calibration
KNOWN_WIDTH = 1.8   # Average vehicle width (meters)
FOCAL_LENGTH = 600  # Camera focal length constant

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Netlify Dashboard Connected Successfully!")
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # AI Object Detection
            results = model(frame, stream=True, verbose=False)
            detected_objects = 0
            min_distance = 999.0
            alert_status = "SAFE"

            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    label = model.names[cls]

                    if label in ['car', 'bus', 'truck', 'motorbike', 'person']:
                        detected_objects += 1
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        box_width = x2 - x1

                        if box_width > 0:
                            dist = (KNOWN_WIDTH * FOCAL_LENGTH) / box_width
                            if dist < min_distance:
                                min_distance = dist

            # Critical Safety Logic
            if min_distance < 2.0:
                alert_status = "CRITICAL_BRAKE"
            elif min_distance < 4.0:
                alert_status = "WARNING"

            # Telemetry Data Packet
            telemetry_data = {
                "objects_count": detected_objects,
                "min_distance": round(min_distance, 2) if min_distance != 999.0 else 0.0,
                "status": alert_status,
                "system_health": "SYSTEM OK",
                "speed": "45 km/h"  # Connect python-obd speed here
            }

            # Send Telemetry to Frontend
            await websocket.send_text(json.dumps(telemetry_data))
            await asyncio.sleep(0.03)  # Real-time stream

    except WebSocketDisconnect:
        print("Netlify Dashboard Disconnected")
    finally:
        cap.release()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
